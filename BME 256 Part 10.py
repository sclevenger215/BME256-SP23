import matplotlib.pyplot as plt
import numpy as np

#Importing initial values
nsteps = [100, 1000, 10000, 100000] #Vector to test nsteps values
bigN = 500 #Number of velocity values to generate
deltaP = 1333 #dynes/cm^2
mu = 0.035 #dyne-sec/cm^2
vseed = 20 #cm/sec

#Initial artery size
r2 = 0.3 #cm
r1 = 0.1 #cm
L = 5 #cm
legend = nsteps

dr = r2 / bigN #cm
radii = np.arange(0, r2, dr) #Creating a vector of the incremented radii for plotting

for k in nsteps: #To calculate and plot the velocities with different values of nsteps on the same graph
    v = np.zeros(bigN + 1) #Creating a vector to store values in
    v.fill(vseed) #Initializing the vector values to vseed
    v[bigN:] = 0
    for i in range(k): #Incrementing nsteps times
        for n in range(bigN): #Calculating velocity for each node
            #Only calculating the velcoity if the radius is bigger than r1 and less than r2
            if n * dr > r1 and n * dr < r2:
                v[n] = 0.5 * (deltaP * dr**2 / mu / L + (1 + 0.5 / n) * v[n + 1] + (1 - 0.5 / n) * v[n - 1])
            else:
                v[n] = 0
    
    # Plotting the velocity vs radius with titles and axis labels
    plt.plot(radii, v[:bigN])
    plt.title('Axial Velocity')
    plt.xlabel('Radius (cm)')
    plt.ylabel('Velocity (cm/s)')
    plt.legend(legend)
