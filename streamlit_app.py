import pandas as pd
from heapq import heapify, heappop, heappush

class Graph:
	def __init__(self):
		self.neighbours_list = {}
		self.no_of_nodes = 0
		self.vertex_data = {}

	# add rmv NODES/VERTICES
	def add_vertex_data(self, vertex, data): #for vertex. node.
		self.vertex_data[vertex] = data
		self.neighbours_list[vertex]={}
		self.no_of_nodes+=1

	def remove_vertex_data(self, vertex):
		#call remove edge first, then remove entire vertex from vertex_data and neighbours_list
		#count remove 1
		pass

	# add rmv CONNECTIONS/EDGES
	def add_edge(self, start, end, time):
		if start in self.vertex_data and end in self.vertex_data:
			self.neighbours_list[start][end] = time

	def remove_edge(self, start, end):
		#call remove edge for all edges connected to this vertex: first remove on this side, then use the key to remove on the other side
		pass

	# getters
	def get_all_station_code(self, station_name):
		#preprocess
		station_name = station_name.lower().strip()
		codes = [k for k, v in self.vertex_data.items() if v.lower() == station_name]
		return codes # CURRENTLY ONLY RETURNS THE FIRST !!!!!!!!
	
	def get_station_code(self, station_name):
		return self.get_all_station_code(station_name)[0]
	
	def get_station_name(self, station_code):
		name = self.vertex_data[station_code]
		return name
	
	# helper functions for dijkstra
	def shortest_time(self, source_stn):
		# init time list
		time_to={node:float('inf') for node in self.vertex_data.keys()}
		time_to[source_stn] = 0

		# init priority queue
		pq = [(0,source_stn)] #1. start with start node
		heapify(pq)

		# record visited nodes
		visited = []
		path =[source_stn]

		#iterate through list
		while pq: #pq is not empty (aka there's reachable nodes you haven't calculated dist. for yet.)
			curr_time, curr_node = heappop(pq)
			if curr_node in visited: #3. if already visited, remove without doing anything.
				continue
			visited.append(curr_node)

			for neighbour, timedist in self.neighbours_list[curr_node].items(): #2. append all neighbours onto PQ; for subsequent runs, append neighbour's neighbours onto PQ
				temp = curr_time + timedist
				if temp < time_to[neighbour]:
					time_to[neighbour] = temp #replace

					heappush(pq, (temp, neighbour))
		
		return time_to
	
	def retrace(self, start, end, time, time_to):
		return self._retrace(start, end, time, time_to)+[end]
	
	def _retrace(self, start, end, time, time_to):
		'''
		init running counter for to_end (confirmed nodes.)
		if time_to[neighbour]==timedist: then return [neighbour]
		if (time)=dist_from_neighbour_to_curr + time_to[neighbour], then return [neighbour] + [self.retrace(self, neighbour, end, time-timedist, time_to)]
		'''
		
		#how to update time?
		neighbour_list=self.neighbours_list[end].items()

		#start = TB, end = buona
		if (start==end): #start==end==TB
			return []
		else:
			for neighbour, timedist in neighbour_list:
				if time_to[neighbour]+timedist==time_to[end]: # t(LP->BV) + 2 == t(TB->BV)
					recursion_list=self._retrace(start, neighbour,time-timedist,time_to)
					recursion_list.append(neighbour)
					return recursion_list

	
	# RETURNNNNNN
	def path(self, start=None, end=None):
		if start==None:
			start=input("Begin from: ")
		if end==None:
			end=input("End at: ")
		
		start_code=self.get_station_code(start)
		end_code=self.get_station_code(end)

		time_to=self.shortest_time(start_code)
		result=time_to[end_code]
		path=self.retrace(start_code, end_code, result, time_to)

		print(f"Shortest time from {self.get_station_name(start_code)} ({start_code}) to {self.get_station_name(end_code)} ({end_code}) is {result} minutes.\nPath:")
		self.flatten_path(path)
		return result, path
	
	def flatten_path(self, path):
		'''
		compare curr and next, flatten timings and paths on the same line
		#specify interchanges
		'''
		prev=0
		total_time=0
		total_total=0
		wait=1
		for i in range(len(path)-1):
			name1=self.get_station_name(path[i])
			name2=self.get_station_name(path[i+1])
			if self.same_line(path[i],path[i+1]): # at the end of a line(either interchange or end of list), print the total time for that segment.
				if prev==0:
					print(name1, end="")
					prev=1
				print(f" -> {name2}",end="")
				total_time+=self.neighbours_list[path[i]][path[i+1]]
			elif name1==name2:
				print(f' Time: {total_time} min')
				total_total+=total_time
				total_time=0
				transfer_time=self.neighbours_list[path[i]][path[i+1]]
				print(f"Transfer at {name1} from {path[i]} to {path[i+1]}. Time: {transfer_time} min") #print transfer time.
				print("Maximum waiting time: 5 min")
				wait+=1
				total_total+=transfer_time
				prev=0
		#at end of line, check and clear if not empty
		print(f'Time: {total_total} to {total_total+(wait*5)} min')
		print('\n')

	def interchange(self,code1, code2): #not rly needed tbh
		name=self.get_station_name(code1)
		lst=self.get_all_station_code(name)
		if code2 in lst:
			return True
		else:
			return False

	def same_line(self, code1, code2):
		return (code1[0:2]==code2[0:2])
		
	
	def __str__(self):
		result = "List of nodes:\n"
		for key,value in self.vertex_data.items():
			result += f"{key}: {value}\n"
		return result
	
intervals=pd.read_csv('intervals.csv')
stn_name=pd.read_csv('station_name.csv')

size=len(stn_name)
interval_size=len(intervals)
mrt_map=Graph()

for i in range(size):
    mrt_map.add_vertex_data(stn_name.iloc[i,0],stn_name.iloc[i,1]) #iloc is used to access the data in the dataframe
    
for i in range(interval_size):
    mrt_map.add_edge(intervals.iloc[i,0], intervals.iloc[i,1], int(intervals.iloc[i,2]))
	
mrt_map.path('telok blangah','pasir ris')
