from jsonschema import validate, ValidationError


class SchemaValidator:
    """Utility class for validating data against JSON schemas."""

    @staticmethod
    def validate(data, schema):
        """
        Validate data against a JSON schema.

        Args:
            data: The data to validate
            schema (dict): JSON schema to validate against

        Returns:
            dict: Validation result with success status and errors
        """
        try:
            validate(instance=data, schema=schema)
            return {"valid": True, "errors": None}
        except ValidationError as e:
            return {
                "valid": False,
                "errors": e.message,
                "failed_path": list(e.absolute_path),
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": f"Schema validation error: {str(e)}",
                "failed_path": None,
            }
