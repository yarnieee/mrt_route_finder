import streamlit as st
import pandas as pd
from src.routing_logic import Graph

#cache-- loaded once
@st.cache_resource
def init_mrt_graph():
	intervals=pd.read_csv('data/intervals.csv')
	stn_name=pd.read_csv('data/station_name.csv')

	size=len(stn_name)
	interval_size=len(intervals)
	mrt_map=Graph()

	for i in range(size):
		mrt_map.add_vertex_data(stn_name.iloc[i,0],stn_name.iloc[i,1]) #iloc is used to access the data in the dataframe
		
	for i in range(interval_size):
		mrt_map.add_edge(intervals.iloc[i,0], intervals.iloc[i,1], int(intervals.iloc[i,2]))
	return mrt_map

def flatten_path(graph, path):
	'''
	compare curr and next, flatten timings and paths on the same line
	#specify interchanges
	'''
	#st.info
	prev=0
	total_time=0 #total time for 1 segment
	total_total=0 #total time for trip
	wait=5 #inbetween waiting times
	curr_list = []
	st.write("Maximum waiting time: 5 min")
	for i in range(len(path)-1):
		name1=graph.get_station_name(path[i])
		name2=graph.get_station_name(path[i+1])

		if graph.same_line(path[i],path[i+1]): # at the end of a line(either interchange or end of list), print the total time for that segment.
			if prev==0:
				curr_list.append(name1)
				prev=1
			curr_list.append(name2)
			total_time+=graph.neighbours_list[path[i]][path[i+1]]
		elif name1==name2:
			#print earlier segment
			print_segment = " ➔ ".join(curr_list)
			st.write(print_segment)
			st.write(f' Time: {total_time} min')
			#update counters
			total_total+=total_time
			total_time=0
			curr_list = [] #reset

			#print transfer time
			transfer_time=graph.neighbours_list[path[i]][path[i+1]]
			st.write(f"Transfer at {name1} from {path[i]} to {path[i+1]}. Time: {transfer_time} min") #print transfer time.
			st.write("Maximum waiting time: 5 min")
			wait+=5
			total_total+=transfer_time
			prev=0
	#at end of line, check and clear if not empty
	if total_time >0:
		print_segment = " ➔ ".join(curr_list)
		st.write(print_segment)
		st.write(f' Time: {total_time} min')
		total_total+=total_time
		total_time=0
		curr_list = [] #reset

	st.write(f'Time: {total_total} to {total_total+wait} min')

mrt_map=init_mrt_graph()

#UI component
st.title("MRT Route Finder")
st.write("the realistic estimate of how long your trip will take. factors in interchange and waiting times.")
start=st.selectbox("Start",["Telok Blangah","Kovan","Kent Ridge","Changi Airport","Pasir Ris"])
end=st.selectbox("End",["Tan Kah Kee","Kovan","Kent Ridge","Changi Airport","Pasir Ris"])

#execute
if st.button("Calculate"):
	time, path = mrt_map.path(start,end)
	
	#display
	st.subheader("Suggested Route")
	st.write(f"Shortest time from {start} ({mrt_map.get_station_code(start)}) to {end} ({mrt_map.get_station_code(start)}) is {time} minutes.")

	flatten_path(mrt_map, path)