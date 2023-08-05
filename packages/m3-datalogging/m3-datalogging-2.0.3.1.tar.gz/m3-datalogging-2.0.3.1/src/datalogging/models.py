# coding: utf-8
import uuid
import datetime

from django.db import models
from json_field import JSONField
from json_field.fields import JSONEncoder

from .helpers import get_snapshot
from .enums import EventCode
from datalogging.api import get_user_ip, get_request_token, get_request
from .signals import msg_for_log_signal, log_context_signal, \
    post_snapshot_signal, post_system_event_signal

__author__ = 'Andrey Torsunov'
__contact__ = 'torsunov@bars-open.com'
__docformat__ = 'restructuredtext'


class LogJSONEncoder(JSONEncoder):
    u""" Наследник JSONEncoder, который умеет работать с ugettext. """

    def default(self, o):
        try:
            ret = super(LogJSONEncoder, self).default(o)
        except TypeError:
            ret = unicode(o)
        return ret


class DataLog(models.Model):
    u""" Лог активности пользователей.

    Лог предусматривает отслеживание активности пользователей в системе,
    такой, как удаление/добавление/изменение записей документов, настро
    ек, прав доступа и т.д.

    `guid`:
        Уникальный ИД записи не является primary_key в случае с
        реляционными БД. Его необходимость возникает в момент выгрузки,
        когда несколько логов выгружаются в одну систему и применение
        primary_key из реляционной БД вызвало бы ряд неудобств связанных
        с коллизиями.
        Во избежание коллизий используется uuid с солью.

    `system_type`:
        В качестве подсистемы выступают сервисы(rest, soap), фоновые
        задачи, основное приложение и т.д. Т.е. это по существу среда
        возникновения события, которое следует перехватить.

    `request_token`:
        В рамках одного запроса сущетствует токен по которому можно
        отследить всю активность пользователя в течении запроса.

    """
    guid = models.CharField(
        u'Уникальный идентификатор записи', max_length=64)
    timestamp = models.DateTimeField(
        u'Время совершения действия', auto_now_add=True)
    event_type = models.CharField(
        u'Тип события', max_length=256)
    event_code = models.CharField(
        u'Код события', max_length=32)
    object_id = models.IntegerField(
        u'ID изменяемого объекта', null=True)
    object_type = models.CharField(
        u'Имя модели объекта', max_length=96, null=True)
    object_snapshot = JSONField(
        u'Снимок состояния объекта ', null=True, default='{}',
        encoder=LogJSONEncoder)
    verbose = models.TextField(
        u'Человекопонятное описание события')
    system_type = models.CharField(
        u'Подсистема', max_length=32)
    suid = models.IntegerField(
        u'Идентификатор объекта в подсистеме', null=True)
    ip = models.CharField(
        u'IP адрес', max_length=15)
    context_data = JSONField(
        u'Контекстно-зависимые данные', null=True, encoder=LogJSONEncoder)
    request_token = models.CharField(
        u'Токен запроса', max_length=64, db_index=True)

    def __init__(self, *a, **kw):
        u""" Инициализация записи лога.

        В момент инициализации подставляются данные из контекста,
        определенного в конкретном проекте. Для того, чтобы пере
        дать контекст необходимо подписать обработчик на сигнал
        `log_context_signal`, который должен возвращать словарь
        содержащий в качестве ключей `suid`, `system_type`,
        `event_type`.

        """
        super(DataLog, self).__init__(*a, **kw)

        # При формировании записи лога не передаются параметры,
        # а при вытаскивании данных из базы наоборот.
        if not (a or kw):
            self.context_data = {}
            self.ip = get_user_ip()
            self.guid = uuid.uuid4().hex
            self.request_token = get_request_token()

            request = get_request()
            responses = log_context_signal.send(self, request=request)
            if len(responses) > 0:
                _, log_context = responses[-1]
            else:
                raise NotImplementedError(
                    "`log_context_signal` signal receiver not implemented")

            self.suid = log_context.get('suid')
            self.timestamp = datetime.datetime.now()
            self.event_type = log_context.get('event_type')
            self.system_type = log_context.get('system_type')

    @classmethod
    def _diff_field(cls, instance, attr_name, old_value, name_map):
        u""" Выявление различий значений поля между состояниями модели.

        :param instance: Экземпляр модели
        :param str attr_name: Наименование поля
        :param old_value: Значение поля из предыдущего состояния модели
        :param dict name_map: Поля модели без *_id

        :return tuple: Имя поля, (старое значение, новое значение),
            человекопонятное наименование поля

        """
        alias = attr_name
        if attr_name.endswith('_id') and attr_name[:-3] in name_map:
            alias = attr_name[:-3]
            diff, verbose_name = cls._diff_related_field(
                instance, alias, old_value
            )
        else:
            diff, verbose_name = cls._diff_normal_field(
                instance, alias, old_value
            )

        return alias, diff, verbose_name

    @staticmethod
    def _diff_normal_field(instance, alias, old_value):
        current_value = getattr(instance, alias, None)
        field = instance._meta.get_field_by_name(alias)[0]
        diff = (old_value or u'(не указано)', current_value)
        return diff, field.verbose_name or alias

    @staticmethod
    def _diff_related_field(instance, alias, old_object_id):
        field = instance._meta.get_field_by_name(alias)[0]
        model = field.rel.to
        obj = getattr(instance, alias, None)
        new_val, old_val = unicode(obj), u'(не указано)'

        if old_object_id:
            try:
                old_val = model.objects.get(id=old_object_id)
            except model.DoesNotExist:
                old_val = u'(не найден)'
            else:
                old_val = unicode(old_val)

        return (old_val, new_val), field.verbose_name or alias

    @classmethod
    def get_verbose_msg(cls, log_record, model_instance, **kw):
        u""" Получение человекопонятного описания события.

        Т.к. для каждого проекта формирование описания будет разным
        метод работает через сигнал `msg_for_log_signal`.

        """
        fields_dict = model_instance and model_instance.__dict__.copy() or {}
        responses = msg_for_log_signal.send(
            cls, log_record=log_record,
            model_instance=model_instance,
            fields_dict=fields_dict,
            **kw)

        if len(responses) > 0:
            _, response = responses[0]
        else:
            raise NotImplementedError(
                "`msg_for_log_signal` signal receiver not implemented")

        return response

    @classmethod
    def make_snapshot(cls, instance, event_code):
        u""" Формирование записи лога о состоянии модели.

        Перед сохранением записи лога вызывается сигнал `post_snapshot`,
        где в качестве аргумента передается не сохраненная запись лога,
        что в свою очередь позволяет воздействовать на запись.

        :param instance: Экземпляр модели
        :param event_code: Событие происшедшее с моделью

        """
        log_rec = cls()
        log_rec.object_id = instance.id
        log_rec.object_type = '{0}.{1}'.format(
            instance._meta.app_label,
            instance.__class__.__name__
        )

        log_rec.event_code = event_code

        if event_code != EventCode.DELETE:
            result_diff = {}
            verbose_names = {}
            cur_snapshot = get_snapshot(instance)
            try:
                name_map = instance._meta._name_map
            except AttributeError:
                name_map = instance._meta.init_name_map()

            # Различие в состояниях экземпляра модели
            state_diff = getattr(instance, '_snapshot', set())
            state_diff -= cur_snapshot

            for attr_name, old_value in state_diff:
                alias, field_diff, verbose = cls._diff_field(
                    instance, attr_name, old_value, name_map
                )
                result_diff[alias] = field_diff
                verbose_names[alias] = verbose

            log_rec.context_data['diff'] = result_diff
            log_rec.context_data['field_names'] = verbose_names

        snapshot = instance.__dict__.copy()
        for key in snapshot.keys():
            if key.startswith('_'):
                del snapshot[key]

        log_rec.object_snapshot = snapshot
        log_rec.verbose = cls.get_verbose_msg(log_rec, instance)

        # Если хотя бы один обработчик вернет False, то это будет
        # означать, что запись с логом не нужно сохранять.
        signal_results = post_snapshot_signal.send(cls, log_record=log_rec)
        if False not in signal_results:
            log_rec.save()

    @classmethod
    def make_system_event(cls, event_code, context_data=None, **kw):
        u""" Формирование записи о событии происшедшем в системе.

        Все спецефичные данные о событии обрабатываются через сигнал
        `post_system_event` ровно так же, как в методе `make_snapshot`.

        :param event_code: Событие в системе.
        :param dict context_data: Доп. данные описывающие событие.

        """
        context_data = context_data or {}
        log_rec = cls()
        log_rec.context_data.update(context_data)
        log_rec.event_code = event_code
        log_rec.verbose = cls.get_verbose_msg(log_rec, None, **kw)

        # Если хотя бы один обработчик вернет False, то это будет
        # означать, что запись с логом не нужно сохранять.
        signal_results = post_system_event_signal.send(cls, log_record=log_rec,
            **kw)
        if False not in signal_results:
            log_rec.save()

    class Meta:
        verbose_name = u'Журнал событий'
        db_table = u'data_logging'
