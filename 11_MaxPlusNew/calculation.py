from fastapi import UploadFile
from automaton import Automaton
import utility
from matrix import Matrix
from cmath import inf

def compute(file1: UploadFile, file2: UploadFile, selected_options):
    result = {}
    automaton1 = Automaton(file1)
    automaton2 = Automaton(file2)

    responses = {}
    r = automaton1.sigma.get_matrix()
    responses[r['name']] = r
    r = automaton1.tau.get_matrix()
    responses[r['name']] = r
    for i in range(len(automaton1.transitions)):
        r = automaton1.transitions[i].get_matrix()
        responses[r['name']] = r
    result['automatonB'] = responses

    responses = {}
    r = automaton2.sigma.get_matrix()
    responses[r['name']] = r
    r = automaton2.tau.get_matrix()
    responses[r['name']] = r
    for i in range(len(automaton2.transitions)):
        r = automaton2.transitions[i].get_matrix()
        responses[r['name']] = r
    result['automatonA'] = responses

    # Perform different actions based on selected checkboxes
    for checkbox_text in selected_options:
        tau_A = automaton1.tau # row vector
        tau_B = automaton2.tau # row vector
        tau_A_T = tau_A.transpose() # column vector
        tau_B_T = tau_B.transpose() # column vector
        sigma_A = automaton1.sigma # row vector
        sigma_B = automaton2.sigma # row vector
        sigma_A_T = sigma_A.transpose() # column vector
        sigma_B_T = sigma_B.transpose() # column vector

        if checkbox_text == "forwardSimulation":
            print("----- Forward Simulation -----")
            responses = {}
            # U_1_fs = tau_A \ tau_B
            U_1_fs = utility.right_residual(tau_A, tau_B)
            U_1_fs.name = "U_1_fs"
            U_1_fs.print_matrix()
            r = U_1_fs.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_fs"
                local_min = Matrix(name, [[inf] * U_1_fs.cols for _ in range(U_1_fs.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]
                    
                    U_1_fs_T = U_1_fs.transpose()
                    left = utility.left_residual(utility.multiply(M_x_B, U_1_fs_T), M_x_A)
                    left_T = left.transpose()
                    local_min = utility.matrix_min(local_min, left_T)
                U_2_fs = utility.matrix_min(local_min, U_1_fs)

                if U_1_fs.value == U_2_fs.value or n == 10:
                    break
                else:
                    U_2_fs.name = name
                    U_1_fs = U_2_fs
                    U_1_fs.print_matrix()
                    r = U_1_fs.get_matrix()
                    responses[r['name']] = r
            result['forwardSimulation'] = responses
                    

        if checkbox_text == "backwardSimulation":
            print("----- Backward Simulation -----")
            responses = {}
            # sigma_A \ sigma_B
            U_1_bs = utility.right_residual(sigma_A, sigma_B)
            U_1_bs.name = "U_1_bs"
            U_1_bs.print_matrix()
            r = U_1_bs.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_bs"
                local_min = Matrix(name, [[inf] * U_1_bs.cols for _ in range(U_1_bs.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]
                    
                    right = utility.right_residual(M_x_A, utility.multiply(U_1_bs, M_x_B))
                    local_min = utility.matrix_min(local_min, right)
                U_2_bs = utility.matrix_min(local_min, U_1_bs)

                if U_1_bs.value == U_2_bs.value or n == 10:
                    break
                else:
                    U_2_bs.name = name
                    U_1_bs = U_2_bs
                    U_1_bs.print_matrix()
                    r = U_1_bs.get_matrix()
                    responses[r['name']] = r
            result['backwardSimulation'] = responses

        if checkbox_text == "forwardBisimulation":
            print("----- Forward Bisimulation -----")
            responses = {}
            # (tau_A \ tau_B) i (tau_A / tau_B)
            U_1_fb = utility.matrix_min(utility.right_residual(tau_A, tau_B), utility.left_residual(tau_A_T, tau_B_T))
            U_1_fb.name = "U_1_fb"
            U_1_fb.print_matrix()
            r = U_1_fb.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_fb"
                local_min = Matrix(name, [[inf] * U_1_fb.cols for _ in range(U_1_fb.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]
                    U_1_fb_T = U_1_fb.transpose()

                    left1 = utility.left_residual(utility.multiply(M_x_B, U_1_fb_T), M_x_A)
                    left1_T = left1.transpose()

                    left2 = utility.left_residual(utility.multiply(M_x_A, U_1_fb), M_x_B)

                    left_min = utility.matrix_min(left1_T, left2)
                    local_min = utility.matrix_min(local_min, left_min)
                U_2_fb = utility.matrix_min(local_min, U_1_fb)

                if U_1_fb.value == U_2_fb.value or n == 10:
                    break
                else:
                    U_2_fb.name = name
                    U_1_fb = U_2_fb
                    U_1_fb.print_matrix()
                    r = U_1_fb.get_matrix()
                    responses[r['name']] = r
            result['forwardBisimulation'] = responses
        

        if checkbox_text == "backwardBisimulation":
            print("----- Backward Bisimulation -----")
            responses = {}
            # (sigma_A \ sigma_B) i (sigma_A / sigma_B)
            U_1_bb = utility.matrix_min(utility.right_residual(sigma_A, sigma_B), utility.left_residual(sigma_A_T, sigma_B_T))
            U_1_bb.name = "U_1_bb"
            U_1_bb.print_matrix()
            r = U_1_bb.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_bb"
                local_min = Matrix(name, [[inf] * U_1_bb.cols for _ in range(U_1_bb.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]
                    U_1_bb_T = U_1_bb.transpose()

                    right1 = utility.right_residual(M_x_A, utility.multiply(U_1_bb, M_x_B))
                    right2 = utility.right_residual(M_x_B, utility.multiply(U_1_bb_T, M_x_A))
                    right2_T = right2.transpose()

                    right_min = utility.matrix_min(right1, right2_T)
                    local_min = utility.matrix_min(local_min, right_min)
                U_2_bb = utility.matrix_min(local_min, U_1_bb)

                if U_1_bb.value == U_2_bb.value or n == 10:
                    break
                else:
                    U_2_bb.name = name
                    U_1_bb = U_2_bb
                    U_1_bb.print_matrix()
                    r = U_1_bb.get_matrix()
                    responses[r['name']] = r
            result['backwardBisimulation'] = responses

        if checkbox_text == "forwardBackwardBisimulation":
            print("----- Forward-Backward Bisimulation -----")
            responses = {}
            # (sigma_A / sigma_B) i (tau_A \ tau_B)
            U_1_fbb = utility.matrix_min(utility.left_residual(sigma_A_T, sigma_B_T), utility.right_residual(tau_A, tau_B))
            U_1_fbb.name = "U_1_fbb"
            U_1_fbb.print_matrix()
            r = U_1_fbb.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_fbb"
                local_min = Matrix(name, [[inf] * U_1_fbb.cols for _ in range(U_1_fbb.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]
                    U_1_fbb_T = U_1_fbb.transpose()

                    left = utility.left_residual(utility.multiply(M_x_B, U_1_fbb_T), M_x_A)
                    left_T = left.transpose()

                    right = utility.right_residual(M_x_B, utility.multiply(U_1_fbb_T, M_x_A))
                    right_T = right.transpose()

                    left_right_min = utility.matrix_min(left_T, right_T)
                    local_min = utility.matrix_min(local_min, left_right_min)
                U_2_fbb = utility.matrix_min(local_min, U_1_fbb)

                if U_1_fbb.value == U_2_fbb.value or n == 10:
                    break
                else:
                    U_2_fbb.name = name
                    U_1_fbb = U_2_fbb
                    U_1_fbb.print_matrix()
                    r = U_1_fbb.get_matrix()
                    responses[r['name']] = r
            result['forwardBackwardBisimulation'] = responses

        if checkbox_text == "backwardForwardBisimulation":
            print("----- Backward-Forward Bisimulation -----")
            responses = {}
            # (sigma_A \ sigma_B) i (tau_A / tau_B)
            U_1_bfb = utility.matrix_min(utility.right_residual(sigma_A, sigma_B), utility.left_residual(tau_A_T, tau_B_T))
            U_1_bfb.name = "U_1_bfb"
            U_1_bfb.print_matrix()
            r = U_1_bfb.get_matrix()
            responses[r['name']] = r

            n = 1
            while True:
                n+=1
                name = "U_" + str(n) + "_bfb"
                local_min = Matrix(name, [[inf] * U_1_bfb.cols for _ in range(U_1_bfb.rows)])
                for i in range(len(automaton1.transitions)):
                    M_x_A = automaton1.transitions[i]
                    M_x_B = automaton2.transitions[i]

                    right = utility.right_residual(M_x_A, utility.multiply(U_1_bfb, M_x_B))
                    left = utility.left_residual(utility.multiply(M_x_A, U_1_bfb), M_x_B)

                    right_left_min = utility.matrix_min(right, left)
                    local_min = utility.matrix_min(local_min, right_left_min)
                U_2_bfb = utility.matrix_min(local_min, U_1_bfb)

                if U_1_bfb.value == U_2_bfb.value or n == 10:
                    break
                else:
                    U_2_bfb.name = name
                    U_1_bfb = U_2_bfb
                    U_1_bfb.print_matrix()
                    r = U_1_bfb.get_matrix()
                    responses[r['name']] = r
            result['backwardForwardBisimulation'] = responses
    return result