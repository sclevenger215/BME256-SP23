import matplotlib.pyplot as plt
import numpy as np

#Importing initial values
alpha = 0.99
nsteps = 2000 #Number of incrementations
bigN = 500 #Number of velocity values to generate
deltaP = 1333 #dynes/cm^2
mu = 0.035 #dyne-sec/cm^2
vseed = 20 #cm/sec

#Wire comparison artery size
r2 = 0.25
radius = [0, 0.023, 0.018]
L = 6
legend = ['No Wire', 'Volcano Inc. Wire', 'Phillips FloWire']

dr = r2 / bigN #cm
radii = np.arange(0, r2, dr) #Creating a vector of the incremented radii for plotting

for r1 in radius: #To calculate the flow with different catheter sizes
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
            v[n] = v[n] + alpha * (v[n] - vlast) #Adjust the velocity to the previous iteration
       
    # Plotting the velocity vs radius with titles and axis labels
    plt.plot(radii, v[:bigN])
    plt.title('Axial Velocity')
    plt.xlabel('Radius (cm)')
    plt.ylabel('Velocity (cm/s)')
    plt.legend(legend)
