from functions import *

m = 120  # weight in kilograms
h = 1.8  # height in metres
D1 = 0  # Hypothetical mass centre length 1 (actuator side)
D2 = 0  # Hypothetical mass centre length 2 (cuff side)
M1 = 0  # Hypothetical mass 1 (actuator side)
M2 = 0  # Hypothetical mass 2 (cuff side)



angles = np.linspace(-90, 90, num=180)
distance = np.linspace(100, 1000, num=100)


G = 9.81
L1 = 0.188*h
L2 = 0.145*h
L3 = 0.108*h

a = 0.436 * L1
b = 0.43 * L2
c = 0.506 * L3
W1 = 0.028 * G * m
W2 = 0.016 * G * m
W3 = 0.006 * G * m

print("Upper arm: ", round(W1 /G, 3), " kg, ", round(L1, 3), " m")
print("Forearm: ", round(W2 / G, 3), " kg, ", round(L2, 3), " m")
print("Hand: ", round(W3 / G, 3), " kg, ", round(L3, 3), " m")

M = a * W1 + (L1 + b) * W2 + (L1 + L2 + c) * W3
Md = (D1*M1+D2*M2)*G

print(M, " Nm (maximum moment, arm mass)",  Md, " Nm (maximum moment, device)")

Available_torque = 37.5 # Nominal motor torque (Nm)

Mass_allowable = (Available_torque-M)/G

mass = np.zeros(len(distance))
for i in range(len(distance)):
    mass[i] = Mass_allowable/(distance[i]/1000)


makeplot(distance, mass, ["Distance from axis (mm)", "Allowable mass (Kg)","Maximum Allowable Device Mass (without compensation)","Mass Limit.png"], ["Allowable mass"])


moments = np.zeros(len(angles))

for i in range(len(angles)):
    moments[i] = M*np.cos(np.radians(angles[i]))
    #print(moments[i])


makeplot(angles, moments, ["Flexion angle °", "Moment (Nm)","Shoulder Joint Moment","Moment - Shoulder .png"], ["Limb mass"])
