from typing import (
    Any,
    Dict,
    Tuple,
)

from django.db import (
    models,
)
from django.utils.decorators import (
    classproperty,
)

from edu_rdm_integration.models import (
    RegionalDataMartEntityEnum,
    RegionalDataMartModelEnum,
)
from edu_rdm_integration.utils import (
    camel_to_underscore,
)
from m3_db_utils.mixins import (
    BaseEnumRegisterMixin,
)
from m3_db_utils.models import (
    ModelEnumValue,
)


class EntityEnumRegisterMixin(BaseEnumRegisterMixin):
    """Миксин, для регистрации сущности в RegionalDataMartEntityEnum."""

    enum = RegionalDataMartEntityEnum
    """Модель-перечисление в которую регистрируется сущность."""

    main_model_enum: ModelEnumValue
    """Значение RegionalDataMartModelEnum, 
    основной модели РВД для формирования сущности."""

    additional_model_enums: Tuple[ModelEnumValue] = ()
    """Перечень дополнительных значений RegionalDataMartModelEnum, 
    которые участвуют в формировании записей сущностей"""

    title: str
    """Расшифровка сущности модели-перечисления"""

    @classproperty
    def key(cls) -> str:
        return camel_to_underscore(cls.__name__.rsplit('Entity', 1)[0], upper=True)

    @classmethod
    def get_register_params(cls) -> Dict[str, Any]:
        register_params = super().get_register_params()
        register_params['main_model_enum'] = cls.main_model_enum
        register_params['entity'] = cls
        register_params['additional_model_enums'] = cls.additional_model_enums

        return register_params


class ModelEnumRegisterMixin(BaseEnumRegisterMixin):
    """Миксин, для регистрации модели в RegionalDataMartModelEnum."""

    enum = RegionalDataMartModelEnum
    """Модель-перечисление в которую регистрируется модель."""

    creating_trigger_models: Tuple[models.Model] = ()
    """Перечень моделей по которым генерируются логи."""

    loggable_models: Tuple[models.Model] = ()
    """Перечень моделей по которым собираются логи."""

    @classproperty
    def key(cls) -> str:
        return camel_to_underscore(cls.__name__).upper()

    @classproperty
    def title(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_register_params(cls) -> Dict[str, Any]:
        register_params = super().get_register_params()
        register_params['model'] = cls
        register_params['creating_trigger_models'] = cls.creating_trigger_models
        register_params['loggable_models'] = cls.loggable_models

        return register_params
