__author__ = 'gia'

from flask import abort


class BaseApi:
    def __init__(self):
        pass

    _resource_name = ''

    def get(self, q=None):
        abort(404, message="Method GET is not implemented")

    def put(self):
        abort(404, message="Method PUT is not implemented")

    def post(self):
        abort(404, message="Method POST is not implemented")

    def delete(self):
        abort(404, message="Method DELETE is not implemented")

    def make_response(self, data):
        from flask_restful import reqparse
        import json
        parser = reqparse.RequestParser()
        parser.add_argument(
            'fields',
            required=True,
            help='The fields requested to fill up the response object',
            location=['values', 'json']
        )
        args = parser.parse_args()
        fields = args.get('fields')
        results = self.transform(data, json.loads(fields))
        return results

    def transform(self, data, fields):
        if not data or not fields or not isinstance(fields, (list, tuple, dict,)) or len(fields) == 0:
            return None

        if isinstance(data, (list, tuple, dict)):
            results = []
            for d in data:
                results.append(self.transform(d, fields))
            return results
        else:
            result = {}
            for attribute_name in fields:
                attribute_value = getattr(data, attribute_name, None)

                from models import db
                if attribute_value:
                    if isinstance(attribute_value, db.Model):
                        # {dict}
                        sub_fields = fields[attribute_name]
                        # Transform only works with db.Model object
                        attribute_value = (sub_fields and isinstance(sub_fields, (list, tuple, dict,)) and len(
                            sub_fields) and self.transform(
                            attribute_value,
                            sub_fields)) or None
                    else:
                        # TODO: Formatter???
                        # {list}
                        formatters = fields[attribute_name]

                if hasattr(data, attribute_name):
                    result[attribute_name] = attribute_value
            return result
