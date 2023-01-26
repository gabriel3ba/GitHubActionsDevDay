import yaml

structure = {
    "name": str,
    "id": int,
    "debug": bool
}

def validate(obj: dict, schema: dict) -> bool:
    errors = []
    if not isinstance(obj, dict):
        errors.append(f"NOT_A_DICT")
        return errors

    required_keys = set(structure.keys())
    available_keys = set(obj.keys())
    missing, additional, intersection = (
        required_keys - available_keys,
        available_keys - required_keys,
        required_keys & available_keys,
    )

    for key in missing:
        errors.append(f"{key}:MISSING_FIELD")

    for key in additional:
        errors.append(f"{key}:EXTRA_FIELD")

    for key in intersection:
        if isinstance(obj[key], dict):
            errors.extend(validate(obj[key], schema[key]))
        elif not isinstance(obj[key], schema[key]):
            errors.append(f"{key}:INVALID_TYPE")
    return errors

def load_config() -> list:
    with open("./config.yaml") as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    for index,obj in enumerate(config):
        if errors := validate(obj, structure):
            raise TypeError(f"Validation failed at object {index + 1} with {errors}")

if __name__ == "__main__":
    main()
