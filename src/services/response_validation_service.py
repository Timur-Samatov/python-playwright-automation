from src.utils.schema_validator import SchemaValidator


class ResponseValidationService:
    """Handles schema validation for API responses."""

    def __init__(self, enable_validation=True):
        self.enable_validation = enable_validation

    def validate_response(self, data, schema):
        """
        Validate response data against a schema.

        Args:
            data: Response data (dict or list)
            schema: JSON schema dict to validate against

        Returns:
            dict: Validation result with success/errors
        """
        if not self.enable_validation:
            return {"valid": True, "enabled": False}

        if not schema:
            return {"valid": False, "error": "Schema not provided"}

        # For array schemas, validate the entire structure first
        if schema.get("type") == "array" and isinstance(data, list):
            # Validate the array structure and then each item
            return self._validate_array_with_items(data, schema)
        elif isinstance(data, list):
            # If data is list but schema is not array type, validate each item
            return self._validate_list(data, schema)
        else:
            return self._validate_single_item(data, schema)

    def _validate_array_with_items(self, data_list, array_schema):
        """Validate array structure and each item against the item schema."""
        # First validate the entire array structure
        overall_validation = SchemaValidator.validate(data_list, array_schema)

        if not overall_validation["valid"]:
            return overall_validation

        # If array is valid, also validate each item individually for detailed errors
        item_schema = array_schema.get("items")
        if item_schema:
            item_validation = self._validate_list(data_list, item_schema)
            # Combine results - overall success plus item-level details
            return {
                "valid": item_validation["valid"],
                "total_items": item_validation["total_items"],
                "valid_items": item_validation["valid_items"],
                "errors": item_validation["errors"],
            }

        return overall_validation

    def _validate_list(self, data_list, schema):
        """Validate each item in a list against an individual item schema."""
        validation_errors = []
        valid_items = 0

        for i, item in enumerate(data_list):
            item_validation = SchemaValidator.validate(item, schema)
            if item_validation["valid"]:
                valid_items += 1
            else:
                validation_errors.append(
                    {"item_index": i, "errors": item_validation["errors"]}
                )

        return {
            "valid": len(validation_errors) == 0,
            "total_items": len(data_list),
            "valid_items": valid_items,
            "errors": validation_errors if validation_errors else None,
        }

    def _validate_single_item(self, data, schema):
        """Validate a single item response."""
        return SchemaValidator.validate(data, schema)
