import plotly.graph_objs as go

class Expense:
    def __init__(self):
        self.labels = ['Transport', 'Food', 'Cloth', 'Others']
        self.pie_values = [0, 0, 0, 0]
        self.fig1 = go.Figure(data=go.Pie(labels=self.labels, values=self.pie_values))
        self.fig2 = go.Figure(data=[go.Scatter(x=[1990, 2000, 2010], y=[4, 1, 2])])

    def update_pie_chart(self, records):
        self.pie_values = [0, 0, 0, 0]
        for record in records:
            if record['Category'] == 'Transport':
                self.pie_values[0] += 1
            elif record['Category'] == 'Food':
                self.pie_values[1] += 1
            elif record['Category'] == 'Cloth':
                self.pie_values[2] += 1
            else:
                self.pie_values[3] += 1
        return go.Figure(data=go.Pie(labels=self.labels, values=self.pie_values))

    def update_line_chart(self, records):
        x = []
        for record in records:
            year = record['Timestamp'].split('-')[0]
            month = record['Timestamp'].split('-')[1]
            period = year + '-' + month
            if period not in x:
                x.append(period)
        x.sort()
        y = [0] * len(x)
        for record in records:
            year = record['Timestamp'].split('-')[0]
            month = record['Timestamp'].split('-')[1]
            period = year + '-' + month
            index = x.index(period)
            y[index] += float(record['Amount'].split('$ ')[1])
        return go.Figure(data=[go.Scatter(x=x, y=y)])
