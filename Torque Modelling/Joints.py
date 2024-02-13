import numpy as np
import matplotlib.pyplot as plt
import functions as fc

Weight = 120   # Weight in kilograms
Height = 1800  # Height in millimetres
print("Body mass: ", Weight, " kg, Height: ", Height/1000, " m")
Fx = 0  # Applied horizontal load to fingers (positive towards shoulder)
Fy = 0  # Applied vertical load on hand (at half-length of the hand, positive down)
t1 = 0  # Shoulder position in degrees from horizontal
t2 = 0  # Elbow position in degrees from the upper arm
t3 = 0  # Wrist position in degrees from the forearm
g = 9.81  # Gravity constant (m/s^2)

Weight = fc.newtons(Weight, g)  # Converts mass into newtons
W1 = 0.028 * Weight             # Calculates segment weights
W2 = 0.016 * Weight
W3 = 0.006 * Weight
L1 = 0.188 * Height / 1000      # Calculates segment lengths
L2 = 0.145 * Height / 1000
L3 = 0.108 * Height / 1000
t1 = fc.deg2rad(t1)             # Converts angles to radians
t2 = fc.deg2rad(t2)
t3 = fc.deg2rad(t3)

print("Upper arm: ", round(W1 / g, 3), " kg, ", round(L1, 3), " m")
print("Forearm: ", round(W2 / g, 3), " kg, ", round(L2, 3), " m")
print("Hand: ", round(W3 / g, 3), " kg, ", round(L3, 3), " m")

print("\n Shoulder:")

# Shoulder joint calculations
Rx1 = Fx*np.cos(t3)-Fy*np.sin(t3)
Ry1 = Fx*np.sin(t3)+Fy*np.cos(t3)+W1+W2+W3
Rm1 = ((0.436*L1*np.cos(t1)*W1)+((L1*np.cos(t1)+0.43*L2*np.cos(t2))*W2)+(L1*np.cos(t1)+L2*np.cos(t2)+0.506*L3*np.cos(t3))*W3)
Rm1 = Rm1 + (L1*np.cos(t1)+L2*np.cos(t2)+L3*np.cos(t3)/2)*Fy*np.cos(t3)   # Fy, x component
Rm1 = Rm1 + (L1*np.sin(t1)+L2*np.sin(t2)+L3*np.sin(t3)/2)*Fy*np.sin(t3)   # Fy, y component
Rm1 = Rm1 + (L1*np.cos(t1)+L2*np.cos(t2)+L3*np.cos(t3))*Fx*np.sin(t3)     # Fx, x component
Rm1 = Rm1 - (L1*np.sin(t1)+L2*np.sin(t2)+L3*np.sin(t3))*Fx*np.cos(t3)     # Fx, y component

X1 = -Rx1
Y1 = -Ry1
M1 = -Rm1
print("X1 = ", fc.rnd(round(X1,3)), " N, Y1 = ", fc.rnd(round(Y1,3)), " N, M1 = ", fc.rnd(round(M1, 3)), " Nm")

print("\n Elbow:")

# Elbow joint calculations
Rx2 = Fx*np.cos(t3)-Fy*np.sin(t3)
Ry2 = Fx*np.sin(t3)+Fy*np.cos(t3)+W1+W2+W3
Rm2 = (((0.43*L2*np.cos(t2))*W2)+(L2*np.cos(t2)+0.506*L3*np.cos(t3))*W3)
Rm2 = Rm2 + (L2*np.cos(t2)+L3*np.cos(t3)/2)*Fy*np.cos(t3)   # Fy, x component
Rm2 = Rm2 + (L2*np.sin(t2)+L3*np.sin(t3)/2)*Fy*np.sin(t3)   # Fy, y component
Rm2 = Rm2 + (L2*np.cos(t2)+L3*np.cos(t3))*Fx*np.sin(t3)     # Fx, x component
Rm2 = Rm2 - (L2*np.sin(t2)+L3*np.sin(t3))*Fx*np.cos(t3)     # Fx, y component

X2 = -Rx2
Y2 = -Ry2
M2 = -Rm2
print("X2 = ", fc.rnd(round(X2,3)), " N, Y2 = ", fc.rnd(round(Y2,3)), " N, M2 = ", fc.rnd(round(M2, 3)), " Nm")

print("\n Wrist:")
# Wrist joint calculations
Rx3 = Fx*np.cos(t3)-Fy*np.sin(t3)
Ry3 = Fx*np.sin(t3)+Fy*np.cos(t3)+W1+W2+W3
Rm3 = 0.506*L3*np.cos(t3)*W3
Rm3 = Rm3 + (L3*np.cos(t3)/2)*Fy*np.cos(t3)   # Fy, x component
Rm3 = Rm3 + (L3*np.sin(t3)/2)*Fy*np.sin(t3)   # Fy, y component
Rm3 = Rm3 + (L3*np.cos(t3))*Fx*np.sin(t3)     # Fx, x component
Rm3 = Rm3 - (L3*np.sin(t3))*Fx*np.cos(t3)     # Fx, y component

X3 = -Rx3
Y3 = -Ry3
M3 = -Rm3
print("X3 = ", fc.rnd(round(X3,3)), " N, Y3 = ", fc.rnd(round(Y3,3)), " N, M3 = ", fc.rnd(round(M3, 3)), " Nm")


## Visualisation
Shoulder = [0,0]                        # Define shoulder coordinates
Elbow = [L1*np.cos(t1),L1*np.sin(t1)]   # Calculate elbow joint position
Wrist = [(Elbow[0]+L2*np.cos(t2)),(Elbow[1]+L2*np.sin(t2))]     # Calculate wrist joint position
Hand = [(Wrist[0]+L3*np.cos(t3)), (Wrist[1]+L3*np.sin(t3))]     # Calculate hand position

# Plot segments
fig = plt.figure()
ax = fig.add_subplot()
plt.plot([0, 1000*Elbow[0]],[0, 1000*Elbow[1]], linewidth = 5, color = 'red')
plt.plot([1000*Elbow[0],1000*Wrist[0]],[1000*Elbow[1],1000*Wrist[1]], linewidth = 5, color = 'blue')
plt.plot([1000*Wrist[0],1000*Hand[0]],[1000*Wrist[1],1000*Hand[1]], linewidth = 5, color = 'green')

ax.set_aspect('equal', adjustable='box')
plt.xlim(-100,800)
plt.ylim(-800,800)
plt.grid()
plt.show()