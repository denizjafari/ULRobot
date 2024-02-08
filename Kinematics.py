import numpy as np
import math

# All angles in degrees. Where a range of motion lies partially along the range, use negative values to specify the
# opposite direction to the listed description
ABD = 0      # Shoulder abduction from vertically downward
FLX = 0      # Shoulder flexion from vertically downward
MEDROT = 0   # Shoulder rotation from neutral position
EFLX = 0     # Elbow flexion from full extension
WFLX = 0     # Wrist flexion from neutral position
WDEV = 0     # Wrist deviation from neutral position
WSUP = 0     # Wrist supination from neutral position

L1 = 500  # Length of upper arm, in millimetres. From GH joint to elbow.
L2 = 400  # Length of forearm, in millimetres. From elbow to wrist joint.

T = [0,-ABD,90-FLX, MEDROT,-90-EFLX,WFLX,90-WDEV,-WSUP]  #DH table developed from diagrams
A = [-90,90,90, -90 , -90,90, 90, 0]
R = [0,0, 0, 0, -L2, 0, 0, 0]
D = [0, 0, 0, -L1, 0, 0, 0, 0]

T = [x*math.pi/180 for x in T]   # Convert angles in T and A lists into radians
A = [x*math.pi/180 for x in A]


for i in range(len(T)-1):   # Loop through the number of table rows (list length T), and transform parameters to find the next
    # segment position and angle

    DH_matrix = np.zeros((4, 4))
    t1 = T[i]
    t2 = T[i+1]
    a1 = A[i]
    a2 = A[i+1]
    d2 = D[i+1]

    DH_matrix[0, :] = [np.cos(t2), -np.sin(t2), 0, R[i]]
    DH_matrix[1, :] = [np.sin(t2) * np.cos(a1), np.cos(t2) * np.cos(a1), -np.sin(a1), -np.sin(a1) * d2]
    DH_matrix[2, :] = [np.sin(t2) * np.sin(a1), np.cos(t2) * np.sin(a1), np.cos(a1), np.cos(a1) * d2]
    DH_matrix[3, :] = [0, 0, 0, 1]

    DH_matrix.round(3,DH_matrix)
    if i != 0:
        DH_matrix = np.dot(DH_prev,DH_matrix)
    if i == 3:
        Elbow_position = DH_matrix # Save final elbow position as a point of interest
    if i ==6:
        Hand_position = DH_matrix # Save hand position as a point of interest
    #print("DH matrix origin to matrix no %d" % i)
    #print(DH_matrix)
    DH_prev = DH_matrix
print("\n Elbow position matrix:")
print(Elbow_position)
print("\n Hand position matrix:")
print(Hand_position)
