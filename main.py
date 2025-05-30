import pandas as pd

class Graph:
	def __init__(self, size):
		self.adj_matrix = {}
		self.size = size
		self.count = 0
		self.vertex_data = {}

	def add_edge(self, start, end, time):
		if start in self.vertex_data and end in self.vertex_data:
			self.adj_matrix[start][end] = time

	def add_vertex_data(self, vertex, data): #for vertex
		self.vertex_data[vertex] = data
		self.adj_matrix[vertex]={}
		self.count+=1

	def remove_vertex_data(self, vertex):
		#call remove edge first, then remove entire vertex from vertex_data and adj_matrix
		#for each item in the rmv_edge's sublist, go to the respective edge and remove rmv_edge from its sublist
        #then remove the rmv_edge
        #count remove 1
		pass

	def remove_edge(self, start, end):
		#call remove edge for all edges connected to this vertex: first remove on this side, then use the key to remove on the other side
		pass

	def get_station_code(self, station_name):
		codes = [k for k, v in self.vertex_data.items() if v == station_name]
		return codes
	
	def get_station_name(self, station_code):
		name = self.vertex_data[station_code]
		return name
		
	def dijkstra(self, start_name):
		start_code = self.get_station_code(start_name) #get code of station by name
		distances = [float('inf')] * self.count
		distances[start_code] = 0
		visited = [False] * self.count

		for _ in range(self.size):
			min_distance = float('inf') #set to +ve infinity value
			u = None
			for i in range(self.size):
				if not visited[i] and distances[i] < min_distance:
					min_distance = distances[i]
					u = i

			if u is None:
				break

			visited[u] = True

			for v in range(self.size):
				if self.adj_matrix[u][v] != 0 and not visited[v]:
					alt = distances[u] + self.adj_matrix[u][v]
					if alt < distances[v]:
						distances[v] = alt
		
		return distances
	
	def __str__(self):
		result = "List of nodes:\n"
		for key,value in self.vertex_data.items():
			result += f"{key}: {value}\n"
		return result

#load data
intervals=pd.read_csv('intervals.csv')
stn_name=pd.read_csv('station_name.csv')

#preprocess
intervals=intervals.map(lambda x: x.strip() if isinstance(x, str) else x)
stn_name=stn_name.map(lambda x: x.strip() if isinstance(x, str) else x)

#save dataframe as csv
#intervals.to_csv('intervals.csv', index=False)
#stn_name.to_csv('station_name.csv', index=False)

#fonstruct graph
size=len(stn_name)
interval_size=len(intervals)
mrt_map=Graph(size)

#construct graph
for i in range(size):
    mrt_map.add_vertex_data(stn_name.iloc[i,0],stn_name.iloc[i,1]) #iloc is used to access the data in the dataframe
    
for i in range(interval_size):
    mrt_map.add_edge(intervals.iloc[i,0], intervals.iloc[i,1], int(intervals.iloc[i,2]))
    
with open('mrt_map_dict.txt','w') as file:
    for key, value in mrt_map.adj_matrix.items():
    	file.write(f"{key}: {value}")
        
#test for correct station
mrt_map.get_station_code("Outram Park")
# mrt_map.get_station_name('NE3')

#use algorithm to get shortest distances
mrt_map.dijkstra("TE11")