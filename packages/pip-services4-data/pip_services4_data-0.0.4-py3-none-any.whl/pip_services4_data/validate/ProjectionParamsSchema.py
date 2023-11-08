from pip_services4_commons.convert import TypeCode

from ..validate.ArraySchema import ArraySchema


class ProjectionParamsSchema(ArraySchema):
    """
    Schema to validate :class:`ProjectionParams <pip_services3_commons.data.ProjectionParams.ProjectionParams>`
    """
    def __init__(self):
        """
        Creates a new instance of validation schema.
        """
        super().__init__(TypeCode.String)
