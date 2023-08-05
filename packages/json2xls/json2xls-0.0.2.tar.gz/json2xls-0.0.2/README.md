json2xls:根据json数据生成excel表格
==================================

[![](https://badge.fury.io/py/json2xls.png)](http://badge.fury.io/py/json2xls)
[![](https://pypip.in/d/json2xls/badge.png)](https://pypi.python.org/pypi/json2xls)


**安装**

    pip install json2xls

**根据json数据生成excel**

code:

    :::python
    from json2xls import Json2Xls

    json_data = '{"name": "ashin", "age": 16, "sex": "male"}'
    Json2Xls('test.xls', json_data).make()

command:

    python json2xls.py test.xls '{"a":"a", "b":"b"}'
    python json2xls.py test.xls '[{"a":"a", "b":"b"},{"a":1, "b":2}]'

    # from file: json of text
    python json2xls.py test.xls "`cat data.json`"

    # from file: json of line
    python json2xls.py test.xls data2.json

excel:

    age | name | sex
    ----|------|----
    30  | John | male
    18  | Alice| female


**根据请求url返回的json生成excel**

默认请求为get，get请求参数为params={}, post请求参数为data={}

code:

    :::python
    from json2xls import Json2Xls

    url = 'http://api.bosonnlp.com/sentiment/analysis'
    Json2Xls('test.xlsx', url, method='post').make()

command:

    python json2xls.py test.xls http://api.map.baidu.com/telematics/v3/weather\?location\=%E4%B8%8A%E6%B5%B7\&output\=json\&ak\=640f3985a6437dad8135dae98d775a09

excel:

    status | message
    -------|--------
    403    | no token header

**自定义title和body的生成**

默认只支持一层json的excel生成，且每天记录字段都相同。如果是多层套嵌的json，请自定义生成title和body，只需定义`title_callback`和`body_callback`方法，在调用`make`的时候传入即可。

    :::python
    def title_callback(self, data):
        '''use one data record to generate excel title'''
        self.sheet.write_merge(0, 0, 0, 3, 'title', self.title_style)
        self.sheet.write_merge(1, 2, 0, 0, 'tag', self.title_style)
        self.sheet.write_merge(1, 2, 1, 1, 'ner', self.title_style)
        self.sheet.write_merge(1, 1, 2, 3, 'comment', self.title_style)
        self.sheet.row(2).write(2, 'x', self.title_style)
        self.sheet.row(2).write(3, 'y', self.title_style)

        self.sheet.write_merge(0, 0, 4, 7, 'body', self.title_style)
        self.sheet.write_merge(1, 2, 4, 4, 'tag', self.title_style)
        self.sheet.write_merge(1, 2, 5, 5, 'ner', self.title_style)
        self.sheet.write_merge(1, 1, 6, 7, 'comment', self.title_style)
        self.sheet.row(2).write(6, 'x', self.title_style)
        self.sheet.row(2).write(7, 'y', self.title_style)

        self.start_row += 3


    def body_callback(self, data):

        key1 = ['title', 'body']
        key2 = ['tag', 'ner', 'comment']

        col = 0
        for ii, i in enumerate(key1):
            for ij, j in enumerate(key2):
                if j != 'comment':
                    value = ', '.join(data[ii][i][j])
                    self.sheet.col(col).width = (len(value) + 1) * 256
                    self.sheet.row(self.start_row).write(col, value)
                    col += 1
                else:
                    for x in data[ii][i][j].values():
                        width = self.sheet.col(col).width
                        new_width = (len(x) + 1) * 256
                        self.sheet.col(col).width = width if width > new_width else new_width
                        self.sheet.row(self.start_row).write(col, x)
                        col += 1
        self.start_row += 1


    data = '''[
                [
                    {
                        "title":
                            {
                                "tag": ["title_tag1", "title_tag2"],
                                "ner": ["title_ner1", "title_ner2"],
                                "comment": { "good": "100", "bad": "20"}
                            }
                    },
                    {
                        "body":
                            {
                                "tag": ["body_tag1", "body_tag2"],
                                "ner": ["body_ner1", "body_ner2"],
                                "comment": { "good": "85", "bad": "60"}
                            }
                    }
                ]
            ]'''

    j = Json2Xls('title_callback.xls', data)
    j.make(title_callback=title_callback, body_callback=body_callback)
