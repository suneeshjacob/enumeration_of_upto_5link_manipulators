import itertools
import numpy
import math
from acrod.functions import all_paths, get_all_combinations_of_two_parts_of_manipulator, all_joints_connected_to_the_link

def kutzbach_dof(M):
    nr = numpy.sum(M==1)
    np = numpy.sum(M==2)
    nc = numpy.sum(M==3)
    ns = numpy.sum(M==4)
    n = len(M)
    return 6*(n-1)-5*(nr+np)-4*nc-3*ns


def are_conditions12_met(M):
    nr = numpy.sum(M==1)
    np = numpy.sum(M==2)
    
    condition1 = nr+np>=1


    if condition1 == False:
        return condition1
    else:
        condition2 = kutzbach_dof(M)>=1
        if condition2 == False:
            return condition2
    
    final_result = condition1 and condition2 # It wil always be True.

    return final_result


    # if condition1 == True:
    #     condition2 = kutzbach_dof(M)>=1
    #     if condition2 == True:
    #         return True
    # return False

    # if fast == True:
    #     if condition1 == False:
    #         return False
    # condition2 = kutzbach_dof(M)>=1
    
    # if fast == True:
    #     return condition1 and condition2
    # else:
    #     return condition1, condition2







def is_condition3_met(M):
    condition3 = True
    n = len(M)
    all_loops = listloops(M)
    all_loops = [i+[i[0]] for i in all_loops]
    
    for j in all_loops:
        indices_of_joints = [sorted([j[j2],j[j2+1]]) for j2 in range(len(j)-1)]
        joints = [M[indices_of_joints[j3][0],indices_of_joints[j3][1]] for j3 in range(len(indices_of_joints))]
        mr = joints.count(1)
        mp = joints.count(2)
        mc = joints.count(3)
        ms = joints.count(4)

        qr = mr + mc + 3*ms - math.comb(ms,2)
        qp = mp + mc
        qt = qr + qp

        if qr < 4:
            if qp < 4:
                condition3 = False
                break
        else:
            if qt < 7:
                condition3 = False
                break

    return condition3



def is_condition4_met(M):
    condition4 = True
    all_loops = listloops(M)
    all_loops = [i+[i[0]] for i in all_loops]
    
    for j in all_loops:
        indices_of_joints = [sorted([j[j2],j[j2+1]]) for j2 in range(len(j)-1)]
        joints = [M[indices_of_joints[j3][0],indices_of_joints[j3][1]] for j3 in range(len(indices_of_joints))]
        mr = joints.count(1)
        mp = joints.count(2)
        mc = joints.count(3)
        ms = joints.count(4)
        qp = mp+mc
        qr = mr+mc+3*ms
        if qr<=3 and qp<=3:
            condition4 = False
            break
    
    return condition4

def iscircular(list1,list2):
    if len(list1)!=len(list2):
        return False
    temp1=' '.join(map(str,list1))
    temp2=' '.join(map(str,list2))
    if len(temp1)!=len(temp2):
        return False
    temp3=temp1+' '+temp1
    if temp2 in temp3:
        return True
    else:
        return False

def reducedcyclic(valueslist):
    for i in range(len(valueslist)):
        if valueslist[i] in valueslist[i+1:]:
            return valueslist[i:i+valueslist[i+1:].index(valueslist[i])+1]

def listloops(A):
    n=len(A)
    a=[]
    for i in range(n):
        temp=[]
        for j in list(range(0,i))+list(range(i+1,n)):
            k=[j,i]
            k.sort()
            if A[k[0],k[1]]!=0:
                temp.append(j)
        a.append(temp)
    
#    temp=[]
    temp5=[]
    for i in range(n):
        temp=[]
        flag=0
        temp.append([i])
        if len(a[i])==0:
            flag=1
            ls=[]
        else:
            temp=[temp[0]+[i2] for i2 in a[i]]
        if flag==0:
            temp2=[]
            for i3 in temp:
                for i4 in a[i3[-1]]:
                    if i4!=i3[-2]:
                        temp2.append(i3+[i4])
        flag2=0
        while flag2==0:
            temp2=[]
            for i3 in temp:
                for i4 in a[i3[-1]]:
                    if i4!=i3[-2]:
                        temp2.append(i3+[i4])
            temp=temp2
            flag2=1
            for i4 in temp:
                if len(set(i4))==len(i4):
                    flag2=0
                    break
        if len(temp)!=0:
            temp6=[]
            for i5 in temp:
                temp8=reducedcyclic(i5)
                if len(temp8)==len(set(temp8)):
                    temp6.append(temp8)
            temp=temp6
            temp5+=temp
    if len(temp5)!=0:
        temp7=[temp5[0]]
        for i in range(len(temp5)):
            for j in range(len(temp7)):
                flag3=0
                if iscircular(temp5[i],temp7[j])==True:
                    flag3=1
                    break
                elif iscircular(temp5[i][::-1],temp7[j])==True:
                    flag3=1
                    break
            if flag3==0:
                temp7.append(temp5[i])
    else:
        temp7=temp5
    return temp7


def encode_graphmatrix(A):
    n = len(A)
    a = []
    c = 0
    inc = 0
    for i in range(n-1):
        inc = n-i-1
        a+=A[i,i+1:].tolist()[0]
        c = c + inc
    return a

def number_of_revolute_and_prismatic(list_of_joints):
    nr = list_of_joints.count(1)
    np = list_of_joints.count(2)
    nc = list_of_joints.count(3)
    ns = list_of_joints.count(4)
    prismatic_number = np+nc
    revolute_number = nr + nc + 3*ns
    return [revolute_number, prismatic_number]



def decode_graphmatrix(a):

    if isinstance(a,str):
        a = list(map(int,list(a)))

    n2 = len(a)
    n = int((1+numpy.sqrt(1+8*n2))/2)
    A = numpy.matrix(numpy.zeros((n,n)),dtype=int)
    c = 0
    inc = 0
    for i in range(n-1):
        inc = n-i-1
        A[i,i+1:] = numpy.matrix(a)[:,c:c+inc]
        c = c + inc
    A = A + A.T
    return A



def graphadjperm(a,l):
    
    if isinstance(a,tuple):
        return tuple(encode_graphmatrix(decode_graphmatrix(a)[l,:][:,l]))
    else:
        return encode_graphmatrix(decode_graphmatrix(a)[l,:][:,l])

def graphmatrix_to_oldmatrix(A_graphmatrix):
    n = A_graphmatrix.shape[0]
    A = A_graphmatrix + numpy.diag([9]*n)
    for i in range(n):
        for j in range(n):
            if i>j:
                A[i,j]=0
    return A

def all_possible_isomorphisms(lst):
    n2 = len(lst)
    n = int((1+numpy.sqrt(1+8*n2))/2)
    output = []
    for i in itertools.permutations(range(1,n-1),n-2):
        output.append(''.join(map(str,graphadjperm(lst,[0]+list(i)+[n-1]))))
    return output

def are_isomorphic(lst1,lst2):
    if lst2 in all_possible_isomorphisms(lst1):
        return True
    return False

from_matrix_to_lst = lambda matrix: sum([matrix[ii,ii+1::].tolist()[0] for ii in range(matrix.shape[0]-1)],[])

change_order = lambda A,l: graphmatrix_to_oldmatrix(decode_graphmatrix(from_matrix_to_lst(A))[l,:][:,l])



def are_conditions45678_met(M):

    n = len(M)
    

    condition4 = True
    condition5 = True
    condition6 = True
    condition7 = True
    condition8 = True
    superfluousdof = 0

    for j2 in get_all_combinations_of_two_parts_of_manipulator(n):
        part1 = list(j2[0])
        part2 = list(j2[1])
        joined_parts = part1 + part2
        coupling_matrix = change_order(M,joined_parts)[:len(part1),-len(part2):]
        number_of_joints_in_coupling_matrix = numpy.sum(coupling_matrix != 0)
        if number_of_joints_in_coupling_matrix == 1:
            if (0 in part1 and n-1 in part1) or (0 in part2 and n-1 in part2):
                condition4 = False
                return condition4, None
                
            else:
                if coupling_matrix[coupling_matrix!=0][0,0] in [3,4]:
                    condition5 = False
                    return condition5, None
                    
        if number_of_joints_in_coupling_matrix >= 2:
            indices_of_nonzero_elements_of_coupling_matrix = numpy.where(coupling_matrix!=0)
            rows_indices_without_repetition = list(set(indices_of_nonzero_elements_of_coupling_matrix[0]))
            columns_indices_without_repetition = list(set(indices_of_nonzero_elements_of_coupling_matrix[1]))
            if len(rows_indices_without_repetition)==1 and len(columns_indices_without_repetition)!=1:
                if 0 in part1 and n-1 in part1:
                    condition6 = False
                    return condition6, None
                    
            elif len(rows_indices_without_repetition)!=1 and len(columns_indices_without_repetition)==1:
                if 0 in part2 and n-1 in part2:
                    condition6 = False
                    return condition6, None
                    
            
            if number_of_joints_in_coupling_matrix == 2:
                if numpy.sum(coupling_matrix==4) == 2:
                    if len(rows_indices_without_repetition)==1 or len(columns_indices_without_repetition)==1:
                        if (0 in part1 and n-1 in part2) or (0 in part2 and n-1 in part1):
                            condition8 = False
                            return condition8, None
                            
                        else:
                            superfluousdof += 1
                    else:
                        condition7 = False
                        return condition7, None
                        
    


    dof = kutzbach_dof(M) - superfluousdof




    final_result = condition4 and condition5 and condition6 and condition7 and condition8 # It wil always be True.


    return final_result, dof



# def are_conditions456789_and_10_met(M):

#     n = len(M)
    

#     condition4 = True
#     condition5 = True
#     condition6 = True
#     condition7 = True
#     condition8 = True
#     condition9 = True
#     condition10 = True
#     superfluousdof = 0

#     for j2 in get_all_combinations_of_two_parts_of_manipulator(n):
#         part1 = list(j2[0])
#         part2 = list(j2[1])
#         joined_parts = part1 + part2
#         coupling_matrix = change_order(M,joined_parts)[:len(part1),-len(part2):]
#         number_of_joints_in_coupling_matrix = numpy.sum(coupling_matrix != 0)
#         if number_of_joints_in_coupling_matrix == 1:
#             if (0 in part1 and n-1 in part1) or (0 in part2 and n-1 in part2):
#                 condition4 = False
#                 return condition4, None
                
#             else:
#                 if coupling_matrix[coupling_matrix!=0][0,0] in [3,4]:
#                     condition5 = False
#                     return condition5, None
                    
#         if number_of_joints_in_coupling_matrix >= 2:
#             indices_of_nonzero_elements_of_coupling_matrix = numpy.where(coupling_matrix!=0)
#             rows_indices_without_repetition = list(set(indices_of_nonzero_elements_of_coupling_matrix[0]))
#             columns_indices_without_repetition = list(set(indices_of_nonzero_elements_of_coupling_matrix[1]))
#             if len(rows_indices_without_repetition)==1 and len(columns_indices_without_repetition)!=1:
#                 if 0 in part1 and n-1 in part1:
#                     condition6 = False
#                     return condition6, None
                    
#             elif len(rows_indices_without_repetition)!=1 and len(columns_indices_without_repetition)==1:
#                 if 0 in part2 and n-1 in part2:
#                     condition6 = False
#                     return condition6, None
                    
            
#             if number_of_joints_in_coupling_matrix == 2:
#                 if numpy.sum(coupling_matrix==4) == 2:
#                     if len(rows_indices_without_repetition)==1 or len(columns_indices_without_repetition)==1:
#                         if (0 in part1 and n-1 in part2) or (0 in part2 and n-1 in part1):
#                             condition8 = False
#                             return condition8, None
                            
#                         else:
#                             superfluousdof += 1
#                     else:
#                         condition7 = False
#                         return condition7, None
                        
    


#     dof = kutzbach_dof(M) - superfluousdof

#     nr = numpy.sum(M==1)
#     np = numpy.sum(M==2)

#     if nr+np < dof:
#         condition9 = False
#         return condition9, None
#     elif dof < 1:
#         condition10 = False
#         return condition10, None



#     final_result = condition4 and condition5 and condition6 and condition7 and condition8 and condition9 and condition10 # It wil always be True.


#     return final_result, dof


def are_conditions_9_10_11_and_12_met(M, dof_i):

    condition9 = True
    condition10 = True
    condition11 = True
    condition12 = True

    nr = numpy.sum(M==1)
    np = numpy.sum(M==2)

    if nr+np < dof_i:
        condition9 = False
        return condition9, None
    elif dof_i < 1:
        condition10 = False
        return condition10, None


    for j in all_paths(M):
        indices_list = [sorted([j[j2],j[j2+1]]) for j2 in range(len(j)-1)]
        joints_list = [M[j2[0],j2[1]] for j2 in indices_list]
        total_dof_from_joints_list = joints_list.count(1) + joints_list.count(2) + 2*joints_list.count(3) + 3*joints_list.count(4)
        if total_dof_from_joints_list < dof_i:
            condition11 = False
            return condition11
    
        if total_dof_from_joints_list == joints_list.count(2):
            if dof_i >= 4:
                condition12 = False
                return condition12
        else:
            if dof_i >= 7:
                condition12 = False
                return condition12

    final_result = condition9 and condition10 and condition11 and condition12 # It wil always be True.
    return final_result

    
# def are_conditions_11_and_12_met(M, dof_i):

#     condition11 = True
#     condition12 = True
#     for j in all_paths(M):
#         indices_list = [sorted([j[j2],j[j2+1]]) for j2 in range(len(j)-1)]
#         joints_list = [M[j2[0],j2[1]] for j2 in indices_list]
#         total_dof_from_joints_list = joints_list.count(1) + joints_list.count(2) + 2*joints_list.count(3) + 3*joints_list.count(4)
#         if total_dof_from_joints_list < dof_i:
#             condition11 = False
#             return condition11
    
#         if total_dof_from_joints_list == joints_list.count(2):
#             if dof_i >= 4:
#                 condition12 = False
#                 return condition12
#         else:
#             if dof_i >= 7:
#                 condition12 = False
#                 return condition12

#     final_result = condition11 and condition12 # It wil always be True.
#     return final_result

possible_joints = [1,2,3,4]
possible_placeholders_for_joints = [0] + possible_joints

n = 4
n2 = int((n**2-n)/2)

matrices = [graphmatrix_to_oldmatrix(decode_graphmatrix(i)) for i in itertools.product(possible_placeholders_for_joints,repeat=n2)]

dof_dictionary = {}


i = 0
all_possible_matrices_before_elimination = len(matrices)
number_of_matrices_after_conditions_1_and_2 = 0
number_of_matrices_after_condition3 = 0
number_of_matrices_after_conditions_456789_and_10 = 0
number_of_matrices_after_conditions_11_and_12 = 0
while i<len(matrices):
    invalid_flag = True
    conditions_1_and_2 = are_conditions12_met(matrices[i])
    if conditions_1_and_2:
        number_of_matrices_after_conditions_1_and_2 += 1
        condition_3 = is_condition3_met(matrices[i])
        if condition_3:
            number_of_matrices_after_condition3 += 1
            conditions456789_and_10, dof = are_conditions456789_and_10_met(matrices[i])
            if conditions456789_and_10:
                number_of_matrices_after_conditions_456789_and_10 += 1
                conditions_11_and_12 = are_conditions_11_and_12_met(matrices[i], dof)
                if conditions_11_and_12:
                    number_of_matrices_after_conditions_11_and_12 += 1
                    invalid_flag = False
                    dof_dictionary[''.join(map(str,encode_graphmatrix(matrices[i])))] = dof
                    i += 1

    if invalid_flag == True:
        matrices.pop(i)



# i = 0
# all_possible_matrices_before_elimination = len(matrices)
# number_of_matrices_after_conditions_1_and_2 = 0
# number_of_matrices_after_condition3 = 0
# number_of_matrices_after_conditions_456789_and_10 = 0
# number_of_matrices_after_conditions_11_and_12 = 0
# while i<len(matrices):
#     invalid_flag = True
#     condition1, condition2 = are_conditions12_met(matrices[i])
#     if condition1 and condition2:
#         number_of_matrices_after_conditions_1_and_2 += 1
#         condition3 = is_condition3_met(matrices[i])
#         if condition3:
#             number_of_matrices_after_condition3 += 1
#             conditions456789_and_10 = are_conditions456789_and_10_met(matrices[i])
#             condition4, condition5, condition6, condition7, condition8, condition9, condition10, dof = conditions456789_and_10
#             if condition4 and condition5 and condition6 and condition7 and condition8 and condition9 and condition10:
#                 number_of_matrices_after_conditions_456789_and_10 += 1
#                 condition11, condition12 = are_conditions_11_and_12_met(matrices[i], dof)
#                 if condition11 and condition12:
#                     number_of_matrices_after_conditions_11_and_12 += 1
#                     invalid_flag = False
#                     dof_dictionary[''.join(map(str,encode_graphmatrix(matrices[i])))] = dof
#                     i += 1

#     if invalid_flag == True:
#         matrices.pop(i)

# i = 0
# while i<len(matrices):
#     invalid_flag = True
#     condition1, condition2 = are_conditions12_met(matrices[i])
#     if condition1 and condition2:
#         condition3 = is_condition3_met(matrices[i])
#         if condition3:
#             conditions456789 = are_conditions456789_met(matrices[i])
#             condition4, condition5, condition6, condition7, condition8, condition9, condition10, dof = conditions456789
#             if condition4 and condition5 and condition6 and condition7 and condition8 and condition9 and condition10:
#                 condition11, condition12 = are_conditions_11_and_12_met(matrices[i], dof)
#                 if condition11 and condition12:
#                     invalid_flag = False
#                     dof_dictionary[''.join(map(str,encode_graphmatrix(matrices[i])))] = dof
#                     i += 1
    
#     if invalid_flag == True:
#         matrices.pop(i)



matrices_string = [''.join(map(str,encode_graphmatrix(i))) for i in matrices]

i = 0
while i<len(matrices):
    isomorphic_flag = False
    for j in all_possible_isomorphisms(matrices_string[i]):
        if j in matrices_string[i+1:]:
            matrices.pop(i)
            matrices_string.pop(i)
            isomorphic_flag = True
            break
    if isomorphic_flag == True:
        pass
    else:
        i += 1



