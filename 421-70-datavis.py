import psycopg2
import sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
	print("please enter the password for cs421g70:")
	pw = str(input())
	connection = psycopg2.connect(user="cs421g70",
		password=pw,
		host="comp421.cs.mcgill.ca",
		port="5432",
		database="cs421")
	query1 = """
		SELECT b.brewery_name, b.street_address, AVG(r.rating) AS avg_rating
		FROM brewery b JOIN rates r 
		ON b.brewery_name=r.brewery_name AND b.street_address=r.street_address
		GROUP BY b.brewery_name, b.street_address
		ORDER BY avg_rating DESC, brewery_name;
	"""
	dat1 = pd.read_sql_query(query1, connection)
	dat1.set_index(['brewery_name', 'street_address'])
	print(dat1.head())

	plt.figure()
	ax1 = dat1.plot.bar(y='avg_rating', rot=0)
	ax1.set_yticks([0, 1, 2, 3, 4, 5])
	ax1.set_xticklabels(dat1.brewery_name, rotation=0)
	ax1.get_legend().remove()
	ax1.set_ylabel('Average Rating (all time)', rotation=90)
	for(x,y) in zip(dat1.index, dat1.avg_rating):
		ax1.text(x-0.1, 0.25, str(round(y, 2)), color='white')
	fig1 = ax1.get_figure()
	plt.savefig('AverageRatings.pdf')
	plt.close()
	
	print('please enter the year of interest')
	yr = int(input())
	prevyr = str(yr-1) + "-12-31 23:59:59"
	curyr = "(" + str(yr) + ")"
	nextyr = str(yr+1) + "-01-01 00:00:00"

	query2 = """
		SELECT t.brewery_name, COUNT(*) AS num_orders
		FROM (SELECT * FROM cust_order o WHERE o.order_status!='cart' 
	  	AND o.order_time>'
	"""
	query2 = query2 + prevyr
	query2 = query2 + """
		' AND o.order_time<'
		"""
	query2 = query2 + nextyr
	query2 = query2+"""
		') AS t
		GROUP BY t.brewery_name
		ORDER BY num_orders DESC, brewery_name;
	"""
	dat2 = pd.read_sql_query(query2, connection)
	dat2.set_index(['brewery_name'])
	print(dat2.head())



	plt.figure()
	ax2 = dat2.plot.bar(y='num_orders', rot=0)
	ax2.set_xticklabels(dat2.brewery_name, rotation=0)
	ax2.get_legend().remove()
	ax2.set_ylabel('Number of Orders '+curyr, rotation=90)
	for(x,y) in zip(dat2.index, dat2.num_orders):
		ax2.text(x-0.1, 0.25, str(y), color='white')
	fig2 = ax2.get_figure()
	plt.savefig('NumOrders.pdf')
	plt.close()

	conn = None


if __name__ == "__main__":
	main()