from flask import Flask, render_template

app=Flask(__name__) # instantiating

@app.route('/plot/')
def plot():
	from pandas_datareader import data 
	import datetime
	from bokeh.plotting import figure, show, output_file
	from bokeh.models.annotations import Title
	from bokeh.embed import components
	from bokeh.resources import CDN

	start=datetime.datetime(2018,1,1)
	end=datetime.datetime(2018,10,31)



	df=data.DataReader(name="AAPL",data_source="yahoo",start=start,end=end)

	p = figure(x_axis_type='datetime', width=1000, height=300)
	t = Title()
	t.text = 'Candlestick Chart'
	p.title=t
	p.grid.grid_line_alpha=0.5
	p.sizing_mode="scale_both"

	hours_12=12*60*60*1000


	def inc_dec(c, o):
		if c > o:
			value="Up"
		elif c < o:
			value="Down"
		else:
			value="Equal"
		return value

	df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close, df.Open)]
	df["Middle"]=(df.Open+df.Close)/2
	df["Height"]=abs(df.Open-df.Close)

	p.segment(df.index, df.High, df.index, df.Low, color="Black")


	p.rect(df.index[df.Status=="Up"], df.Middle[df.Status=="Up"], hours_12, df.Height[df.Status=="Up"],fill_color="#00FF00", line_color="black")
	p.rect(df.index[df.Status=="Down"], df.Middle[df.Status=="Down"], hours_12, df.Height[df.Status=="Down"],fill_color="#B22222", line_color="black")

	script1, div1 =components(p)

	cdn_js=CDN.js_files[0]
	cdn_css=CDN.css_files[0]
	return render_template("plot.html", script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)



@app.route('/') # url
def home():
	return render_template("home.html")

@app.route('/about/') # url
def about():
	return render_template("about.html")

if __name__=="__main__":
	app.run(debug=True)
