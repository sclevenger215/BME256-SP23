import matplotlib.pyplot as plt
import numpy as np

#Importing initial values
alpha = np.arange(0.1, 1, 0.1) #Creates vector to test alpha values
alpha = np.append(alpha, [0.97, 0.98, 0.99]) #Adds a few more values to the alpha vector
for a in range(len(alpha)): #rounds each value of alpha to 2 decimal places
    alpha[a] = round(alpha[a], 2)

nsteps = 2000 #Number of incrementations
bigN = 500 #Number of velocity values to generate
deltaP = 1333 #dynes/cm^2
mu = 0.035 #dyne-sec/cm^2
vseed = 20 #cm/sec

#Initial artery size
r2 = 0.3 #cm
# r1 = 0 #cm
r1 = 0.1 #cm
L = 5 #cm
legend = alpha

dr = r2 / bigN #cm
radii = np.arange(0, r2, dr) #Creating a vector of the incremented radii for plotting

for a in alpha: #To calculate and plot the velocities with different values of alpha on the same graph
    v = np.zeros(bigN + 1) #Creating a vector to store values in
    v.fill(vseed) #Initializing the vector values to vseed
    v[bigN:] = 0
    for i in range(nsteps): #Incrementing nsteps times
        for n in range(bigN): #Calculating velocity for each node
            #Only calculating the velcoity if the radius is bigger than r1 and less than r2
            vlast = v[n] #Save the last iteration's value
            if r1 < dr: #Sets the first value equal to the second if r1 is less than dr
                v[0] = v[1]
            if n * dr > r1 and n * dr < r2:
                v[n] = 0.5 * (deltaP * dr**2 / mu / L + (1 + 0.5 / n) * v[n + 1] + (1 - 0.5 / n) * v[n - 1])
            else:
                v[n] = 0
            v[n] = v[n] + a * (v[n] - vlast) #Adjust the velocity to the previous iteration
        
    # Plotting the velocity vs radius with titles and axis labels
    plt.plot(radii, v[:bigN])
    plt.title('Axial Velocity')
    plt.xlabel('Radius (cm)')
    plt.ylabel('Velocity (cm/s)')
    plt.legend(legend)
