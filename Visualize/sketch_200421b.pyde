photon_goal = [0,100,0]
photon_pos = [0, 0, 0]
base_loc = [0,-200, 0]
photon_moves = [0, 2, 0]
times_to_draw = [5,5,5,5,5]
TRANSMITTED = 1
REFLECTED = 0
ABSORBED = 2
depth = 0
tau_bar = 10
countdown = 2
g = 0.85
wpi = 1
box_height = 400
direction = [0,1,0]
done_count = 0
trans_count = 0
ref_count = 0

def setup():
    size(740,440, P3D)
    background(0)
    start_photon()
    
def draw():
    clear()
    draw_stats()
    draw_box()
    move_photon()
    draw_photon_line()
    
def draw_stats():
     global ref_count, trans_count, tau_bar, g
     est_ref = tau_bar/(2/(1-g)+tau_bar)
     est_trans = 1/((1-g)*tau_bar/2+1)
     total = max(ref_count+trans_count,1)
     translate(0, 0, 0)
     textSize(30)
     text("Reflected Percent: "+str(round(float(ref_count)/total,3))+ "  vs.   2-Stream Approx: "+str(round(est_ref,3)), 0, 0 )
     
     translate(200, 600, 0)
     textSize(30)
     text("Transmitted Percent: "+str(round(float(trans_count)/total,3))+ "  vs.   2-Stream Approx: "+str(round(est_trans,3)), 0, 0 )
     
     translate

def draw_box():
    camera(width/2-100, height/4-100, 3*height/4 /tan(PI/6), width/2, height/2, 0, 0, 1, 0)
    translate(3*width/6, height/2, -100)
    stroke(255)
    noFill()
    box(600, box_height, 400)
    
def set_photon_goal(x,y,z):
    #print("Setting goal to ("+str(x)+", "+str(y)+", "+str(z)+")")
    global photon_goal, times_to_draw, photon_pos
    photon_goal = [x, y, z]
    dist_x = photon_goal[0] - photon_pos[0]
    dist_y = photon_goal[1] - photon_pos[1]
    dist_z = photon_goal[2] - photon_pos[2]
    tot_dist = [dist_x, dist_y, dist_z]
    photon_moves[0] = tot_dist[0]/10
    photon_moves[1] = tot_dist[1]/10
    photon_moves[2] = tot_dist[2]/10
    times_to_draw = [5,5,5,5,5]
    
def draw_photon_line():
    global times_to_draw
    translate(base_loc[0], base_loc[1], base_loc[2])
    translate(photon_pos[0], photon_pos[1], photon_pos[2])
    for i in range(0,5):
        translate(-i/5*photon_moves[0], -i/5*photon_moves[1], -i/5*photon_moves[2])
        if(times_to_draw[i]+i == 5):
            stroke(255, 255, 255, 255-5*(5-i))
            fill(255, 255, 255, 255-5*(5-i))
            sphere(10)
        else:
            times_to_draw[i] = times_to_draw[i] - 1
            break

def mark_if_finished():
    global depth, tau_bar
    if(depth>tau_bar):
        #print("Photon Transmitted!")
        draw_result(TRANSMITTED)
        return 1
    elif(photon_goal[1]<0):
        #print("Photon Reflected!")
        draw_result(REFLECTED)
        return 1
    else:
        return 0

def mark_t_or_r():
    global depth, tau_bar, trans_count, ref_count
    scale_factor = box_height/tau_bar
    if(depth>tau_bar):
        trans_count = trans_count+1
    elif(photon_goal[1]<0):
        ref_count = ref_count+1

def move_photon():
    global photon_pos, photon_move, photon_goal, depth, tau_bar, countdown, done_count
    finished = mark_if_finished()
    dist_left = abs(photon_goal[0]-photon_pos[0])
    dist_left = dist_left + abs(photon_goal[1]-photon_pos[1])
    dist_left = dist_left + abs(photon_goal[2]-photon_pos[2])
    if(dist_left>0.01):
        if(photon_pos[0]+photon_moves[0]>300):
            #print("Move x to "+str(photon_pos[0]+photon_moves[0]) )
            photon_pos[0] = photon_pos[0]+photon_moves[0] - 600
            #print("Adjusted x to "+str(photon_pos[0]) )
            set_photon_goal(photon_goal[0] - 600, photon_goal[1], photon_goal[2] )
        elif(photon_pos[0]+photon_moves[0]<-300):
            #print("Move x to "+str(photon_pos[0]+photon_moves[0]) )
            photon_pos[0] = 600+ photon_pos[0]+photon_moves[0]
            #print("Adjusted x to "+str(photon_pos[0]) )
            set_photon_goal(600 + photon_goal[0], photon_goal[1], photon_goal[2] )
        elif(photon_pos[2]+photon_moves[2]>200):
            #print("Move z to "+str(photon_pos[2]+photon_moves[2]) )
            photon_pos[2] = photon_pos[2]+photon_moves[2] - 400
            #print("Adjusted z to "+str(photon_pos[2]) )
            set_photon_goal(photon_goal[0], photon_goal[1], photon_goal[2] - 400 )
            #print("Adjusted goal z to "+str(photon_goal[2]) )
        elif(photon_pos[2]+photon_moves[2]<-200):
            #print("Move z to "+str(photon_pos[2]+photon_moves[2]) )
            photon_pos[2] = 400 + photon_pos[2]+photon_moves[2]
            #print("Adjusted z to "+str(photon_pos[2]) )
            set_photon_goal(photon_goal[0], photon_goal[1], 400 + photon_goal[2] )
            #print("Adjusted goal z to "+str(photon_goal[2]) )
        else:
            photon_pos[0] = photon_pos[0]+photon_moves[0]
            photon_pos[1] = photon_pos[1]+photon_moves[1]
            photon_pos[2] = photon_pos[2]+photon_moves[2]
    #Reached the goal point
    else:
        if(finished):
            done_count = done_count +1
            if(done_count > 30):
                mark_t_or_r()
                done_count = 0
                photon_pos = [0, 0, 0]
                start_photon()
        else:
            scatter_event()
        
def draw_result(result):
    textSize(32)
    if(result == 0):
        text("Reflected!", 50, 50)
    else:
        text("Transmitted!", 50, 50)

def exp_dist(x):
    return -log(1-x)

def hg_phase_dist(x, g):
    return 1/(2*g)*(1+pow(g,2) - pow((1-pow(g,2))/(1-g+2*g*x), 2))

def draw_random_tau():
    xi = random(1)
    tau = exp_dist(xi)
    return tau

def draw_random_angles(g):
    xi = random(1)
    costheta = hg_phase_dist(xi, g)
    theta = acos(costheta)
    xi = random(1)
    phi = 2*PI*xi
    return [theta, phi]

def make_matrix(theta, phi):
    M0 = [cos(theta)*cos(phi), cos(theta)*sin(phi), -sin(theta)]
    M1 = [-sin(phi), cos(phi), 0]
    M2 = [sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)]
    return [M0, M1, M2]

def scatter_event():
    global wpi, g, depth, direction, photon_pos
    global ABSORBED
    absorb_random = random(1)
    if(absorb_random > wpi):
        #print("Photon Absorbed!")
        return ABSORBED
    #Get next path length
    next_tau = draw_random_tau()
    #Get scattering angles
    [theta, phi] = draw_random_angles(g)
    #Make matrix
    [M0, M1, M2] = make_matrix(theta,phi)
    direction_tau = [0, 0, 0]
    #Calculate movement direction M x direction (matrix vector product)
    direction_tau[0] = dot_product(M0, direction)
    direction_tau[1] = dot_product(M1, direction)
    direction_tau[2] = dot_product(M2, direction)
    #Calculate movement in i,j,k directions with new tau
    delta_tau = [direction_tau[0]*next_tau, direction_tau[1]*next_tau, direction_tau[2]*next_tau]
    #Update depth
    depth = depth + delta_tau[2]
    #print(depth)
    
    direction = [direction_tau[0], direction_tau[1], direction_tau[2]]
    scale_factor = box_height/tau_bar
    #In delta_tau the z component is the height so it gets put into the y component for visualization.
    set_photon_goal(photon_pos[0]+delta_tau[0]*scale_factor, photon_pos[1]+scale_factor*delta_tau[2], photon_pos[2]+scale_factor*delta_tau[1])


# Will return 1 if transmitted, 0 if reflected, 2 if absorbed, and -1 for issues
def start_photon():
    global tau_bar, direction, trans_count, ref_count, depth
    direction = [0,0,1]
    tau = draw_random_tau()
    # theta and phi are 0 on first movement as they are directly incident.
    # This means all movement is in z direction.
    depth = tau
    #print("First tau is "+str(tau))
        
    if(depth>tau_bar):
        #print("Photon Transmitted!")
        draw_result(TRANSMITTED)
        trans_count = trans_count +1
        set_photon_goal(0,box_height/tau_bar*depth, 0)
    elif(depth<0):
        #print("Photon Reflected!")
        ref_count = ref_count + 1
        set_photon_goal(0,box_height/tau_bar*depth, 0)
        draw_result(REFLECTED)
    else:
        set_photon_goal(0,box_height/tau_bar*depth, 0)
    
def dot_product(A,B):
    total = 0
    for i in range(3):
        total = total + A[i]*B[i]
    return total
