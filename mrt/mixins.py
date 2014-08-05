
from flask import request, jsonify
from querystring_parser import parser


class FilterView(object):

    def get(self):
        args = parser.parse(request.query_string)
        columns = []
        for i in range(len(args['columns'])):
            columns.append(args['columns'][i])

        options = {
            'start': args.get('start', 0),
            'limit': args.get('length', 10),
        }

        order = []
        for i in range(len(args['order'])):
            column_id = args['order'][i]['column']
            order.append({
                'column': columns[column_id]['data'],
                'dir': args['order'][i]['dir']
            })
        options['order'] = order

        total = self.get_queryset(count=True)
        rows, filtered = self.get_queryset(**options)

        data = []
        for row in rows:
            row_data = {}
            for column in columns:
                callback = getattr(self, 'process_%s' % column['data'],
                                   lambda row, val: val)
                val = getattr(row, column['data'], None)
                row_data[column['data']] = callback(row, val)
            data.append(row_data)

        return jsonify(recordsTotal=total,
                       recordsFiltered=filtered,
                       data=data)