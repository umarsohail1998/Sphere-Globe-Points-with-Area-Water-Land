def main():
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np
    from matplotlib import animation
    from matplotlib import cm
    import scipy as sp
    import voronoi_utility
    import math
    import pandas as pd
    from tqdm import tqdm
    import json
    import csv
    import time
    from global_land_mask import globe

    radius = float(input("please input your desired radius for sphere: "))
    no_points = int(input("please input your desired number of points: "))



    #calculating the areas of convex polygons
    def polygon_area(poly):
        #shape (N, 3)
        if isinstance(poly, list):
            poly = np.array(poly)
        #all edges
        edges = poly[1:] - poly[0:1]
        # row wise cross product
        cross_product = np.cross(edges[:-1],edges[1:], axis=1)
        #area of all triangles
        area = np.linalg.norm(cross_product, axis=1)/2
        return sum(area)

    def long_lat(array):
        latitude = math.asin(array[2]/radius)
        longitude = math.atan2(array[1], array[0])
        return round(latitude*(180/math.pi), 6),round(longitude*(180/math.pi), 6)

    
    start_time = time.time()

    # pin down the pseudo random number generator (prng) object to avoid certain pathological generator sets
    prng = np.random.RandomState(
        117)  # otherwise, would need to filter the random data to ensure Voronoi diagram is possible
    # produce 1000 random points on the unit sphere using the above seed
    random_coordinate_array = voronoi_utility.generate_random_array_spherical_generators(no_points, radius, prng)
    # produce the Voronoi diagram data
#     print(random_coordinate_array)
    voronoi_instance = voronoi_utility.Voronoi_Sphere_Surface(random_coordinate_array, radius)
#     print(random_coordinate_array)
#     print(voronoi_instance)
    print("*** voronoi_polygon_vertices ***")
    start_time = time.time()
    dictionary_voronoi_polygon_vertices = voronoi_instance.voronoi_region_vertices_spherical_surface()
    # plot the Voronoi diagram
    end_time = time.time()
    print('Total Execution time = %.6f seconds' % (end_time-start_time))

    fig = plt.figure()
    fig.set_size_inches(2, 2)
    ax = fig.add_subplot(111, projection='3d')
    
    
#     start_time = time.time()

    print("*** Creating Files ***")
#     dft = []
#     for generator_index, voronoi_region in dictionary_voronoi_polygon_vertices.items():
#         random_color = colors.rgb2hex(np.random.rand(3))
#         # fill in the Voronoi region (polygon) that contains the generator:
#         polygon = Poly3DCollection([voronoi_region], alpha=1.0)
#         polygon.set_color(random_color)
#         ax.add_collection3d(polygon)
#         list_of_coordinates = []
#         dt = {'land': 0, "water": 0}
#         for array in voronoi_region:
#             ll = long_lat(array)
#             is_on_land = globe.is_land(ll[0], ll[1])
#             is_in_ocean = globe.is_ocean(ll[0], ll[1])
#             if is_on_land:
#                 dt['land']+=1
#             elif is_in_ocean:
#                 dt['water']+=1
#             list_of_coordinates.append("{}".format(list(ll)))
#         area_type = ""
#         if dt['land'] > dt['water']:
#             area_type = "land"
#         else:
#             area_type = "water"    

#         dft.append({'area_id':generator_index,
#                      'area_contained':polygon_area(voronoi_region),
#                      'area_type':area_type,
#                      'latitude_and_longitude':list_of_coordinates})

    
#     df = pd.DataFrame.from_dict(dft)
#     df.to_csv("result.csv")
    
    start_time = time.time()
    #creating required csv file
    with open('result.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['area_id','area_contained', 'area_type', 'latitude_and_longitude'])
        lt = list(dictionary_voronoi_polygon_vertices.keys())
        for i in tqdm(range(len(lt))):
            generator_index = lt[i]
            voronoi_region = dictionary_voronoi_polygon_vertices[generator_index]
#         for generator_index, voronoi_region in dictionary_voronoi_polygon_vertices.items():
            # print(voronoi_region)
            random_color = colors.rgb2hex(np.random.rand(3))
            # fill in the Voronoi region (polygon) that contains the generator:
            polygon = Poly3DCollection([voronoi_region], alpha=1.0)
            polygon.set_color(random_color)
            ax.add_collection3d(polygon)
            list_of_coordinates = []
            dt = {'land': 0, "water": 0}
#             print(len(voronoi_region))
            for array in voronoi_region:
                ll = long_lat(array)
                lat = ll[0]
                lon = ll[1]
                is_on_land = globe.is_land(lat, lon)
                is_in_ocean = globe.is_ocean(lat, lon)
                if is_on_land:
                    dt['land']+=1
                elif is_in_ocean:
                    dt['water']+=1
                list_of_coordinates.append("{}".format(list(ll)))
            area_type = ""
            if dt['land'] > dt['water']:
                area_type = "land"
            else:
                area_type = "water"
            writer.writerow([generator_index,polygon_area(voronoi_region),area_type,list_of_coordinates])

#     print("*** Creating  Json ***")
    with open("result.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
#         print(rows) 
    with open('vernoi.json','w') as f1:
        json.dump(rows,f1)
        
    end_time = time.time()
    print('Total Execution time = %.6f seconds' % (end_time-start_time))
    
    print("*** Displaying Image ***")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xticks([-1, 1])
    ax.set_yticks([-1, 1])
    ax.set_zticks([-1, 1])
    
    plt.tick_params(axis='both', which='major', labelsize=6)
    def animate(i):
        ax.view_init(elev=20, azim=i*4)
        return fig,
    ani = animation.FuncAnimation(fig, animate, frames=90, interval=200, blit=False)
    plt.show()


if __name__=='__main__':
    main()