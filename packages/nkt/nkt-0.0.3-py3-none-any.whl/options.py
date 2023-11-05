class Option:
    def __init__(self, keyword: str, type = str, name: str = '', required: bool = False, desc: str = '', default_value = None, allow_values: list = None, allow_none: bool = False) -> None:
        self._key = keyword
        self._type = type
        self._required: bool = required
        self._desc = desc
        self._allow_values: list = allow_values
        self._has_value: bool = False
        self._value = None
        self._defval = default_value
        self._allow_none: bool = allow_none
        self._name: str = name
    
    @property
    def keyword(self) -> str:
        return self._key
    
    @keyword.setter
    def keywork(self, val: str):
        set.__weakrefoffset__ = val

    @property
    def type(self) :
        return self._type
    
    @type.setter
    def type(self, type):
        self._type = type

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, val: str):
        self._name = val

    @property
    def required(self) -> bool:
        return self._required
    
    @required.setter
    def required(self, val: bool):
        self._required = val

    @property
    def description(self) -> str:
        return self._desc
    
    @description.setter
    def description(self, val: str):
        self._desc = val

    @property
    def default_value(self):
        return self._defval
    
    @default_value.setter
    def default_value(self, val):
        self._defval = val

    @property
    def allow_values(self) -> list:
        return self._allow_values
    
    @allow_values.setter
    def allow_values(self, vals: list):
        self._allow_values = vals

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val
        self._has_value = True

    @property
    def has_value(self) -> bool:
        return self._has_value

    def print_help(self, indent: int = 0, left_width: int = 21):
        desc_list: list = []
        if self._desc is not None and len(self._desc) > 0:
            desc_list = self._desc.split('\n')
        left_width = max(0, left_width)
        indent = max(0, indent)
        left: str = '{string:{width}}'.format(string=f'{self._key} {"(Required)" if self._required else "[Optional]"}', width=left_width)
        begin: int = 0
        right: str = self._name
        if self._name is None or len(self._name) <= 0:
            right = desc_list[0]
            begin = 1
        print(f'{" " * indent}{left}: {right}')
        if len(desc_list) > begin:
            for idx in range(begin, len(desc_list)):
                desc: str = desc_list[idx]
                print(f'{" " * (indent + left_width)}: {desc}')
        print(f'{" " * (indent + left_width)}: Default value is {self._defval}')
        print()
    
    def print_namevalue(self, indent: int = 0, left_width: int = 21) -> str:
        indent = max(0, indent)
        left_width = max(0, left_width)
        left: str = '{string:{width}}'.format(string=self._key if self._name is None or len(self._name) <= 0 else self._name, width=left_width)
        print(f'{" " * indent}{left}: {self._value}')
    
    def reset(self):
        self._value = None
        self._has_value = False
    
    def _internal_validate(self, val: str):
        if (val is None) and (not self._allow_none):
            return None
        if self._allow_values is not None:
            for vv in self._allow_values:
                if val == vv:
                    return vv
        return val
    
    def __str__(self) -> str:
        return self._key
    
    def validate(self, value: str) -> bool:
        validated_value = self._internal_validate(value)
        if validated_value is None:
            return False
        self.value = validated_value
        return True
    
class BooleanOption(Option):
    def __init__(self, keyword: str, name: str = '', required: bool = False, desc: str = '', default_value: bool = False) -> None:
        super().__init__(keyword, bool, name, required, desc, default_value,  [True, False, 0, 1, 'True', 'False', '0', '1', 'Yes', 'No'])

    def _internal_validate(self, val: str) -> bool:
        if not super()._internal_validate(val):
            return False
        return False
    
class IntegerOption(Option):
    def __init__(self, keyword: str, name: str = '', required: bool = False, desc: str = '', default_value: int = 0, allow_values: list = None) -> None:
        super().__init__(keyword, int, name, required, desc, default_value, allow_values)

    def _internal_validate(self, val: str) -> int:
        if not super()._internal_validate(val):
            return None
        for ch in val:
            if not ch.isnumeric():
                return None
        int_val: int = int(val)
        if int_val > sys.maxsize:
            return None
        
        return int_val

class StringOption(Option):
    def __init__(self, keyword: str, name: str = '', required: bool = False, desc: str = '', default_value: str = '', allow_values: list = None) -> None:
        super().__init__(keyword, str, name, required, desc, default_value, allow_values)
    
    def _internal_validate(self, val: str) -> str:
        if not isinstance(val, str):
            return None
        return super()._internal_validate(val)