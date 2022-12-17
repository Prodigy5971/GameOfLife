import pygame
import numpy as np
import random, pyautogui, sys

pygame.init()

screen_width, screen_height = pyautogui.size()
screen_width -= 100; screen_height -= 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GameOfLife")
bg = 25, 25, 25
screen.fill(bg)

celdas = (100, 60)
nxC, nyC = celdas[0], celdas[1]
# dev config 40, 25
min_xC, min_yC = 40, 25
# dev config 100, 50
max_xC, max_yC = 120, 75

dimCW = screen_width / nxC
dimCH = screen_height /nyC
map = [[random.randint(0, 1) for _ in range(nxC)] for _ in range(nyC)]

def neighbors(x, y, map):
    sum = 0
    # right value
    sum += map[(y) % nyC  ][(x+1) % nxC]
    # top right value
    sum += map[(y-1) % nyC][(x+1) % nxC]
    # top value
    sum += map[(y-1) % nyC][(x) % nxC  ]
    # top left value
    sum += map[(y-1) % nyC][(x-1) % nxC]
    # left value
    sum += map[(y) % nyC  ][(x-1) % nxC]
    # bottom left value
    sum += map[(y+1) % nyC][(x-1) % nxC]
    # bottom value
    sum += map[(y+1) % nyC][(x) % nxC  ]
    # bottom right value
    sum += map[(y+1) % nyC][(x+1) % nxC]
    return sum

def grid():
    for y in range(0, nyC):
        for x in range(0, nxC):
            pygame.draw.line(screen, (128, 128, 128), (x * dimCW, 0), (x * dimCW, screen_height), 1)
            pygame.draw.line(screen, (128, 128, 128), (0, y * dimCH), (screen_width, y * dimCH), 1)
grid()

start = False
pause = False
clock = pygame.time.Clock()
running = True
while running:
    if not start: pass
    elif pause: pass
    else:
        #copy of map
        newMap = np.copy(map)
        screen.fill(bg)
        for y in range(0, nyC):
            for x in range(0, nxC):
                # Numbers of live neighbors
                n_neigh = neighbors(x, y, map)
                if(map[y][x] == 0 and n_neigh == 3):
                    newMap[y][x] = 1
                elif(map[y][x] == 1 and (n_neigh < 2 or n_neigh > 3)):
                    newMap[y][x] = 0

                #poly = [((x)     * dimCW, y * dimCH),
                        #((x + 1) * dimCW, y * dimCH),
                        #((x + 1) * dimCW, (y + 1) * dimCH),
                        #((x)     * dimCW, (y + 1) * dimCH)] 
                #pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                ### With lines is more slower than polygon
                #pygame.draw.line(screen, (128, 128, 128), (x * dimCW, 0), (x * dimCW, screen_height), 1)
                #pygame.draw.line(screen, (128, 128, 128), (0, y * dimCH), (screen_width, y * dimCH), 1)
                #pygame.draw.rect(screen, (255, 0, 0), ((2 * dimCW) + 1, (2 * dimCH) + 1, dimCW - 1, dimCH -1))
                if(not newMap[y][x]):
                    pygame.draw.rect(screen, (0, 0, 0), ((x * dimCW) + 0.8, (y * dimCH) + 1, dimCW - 1, dimCH -1))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), ((x * dimCW) + 0.8, (y * dimCH) + 1, dimCW - 1, dimCH -1))
        map = newMap


    # Obtain list of keys pressed
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
        #pass

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE and start):
                pause = not pause
            elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                start = True
        elif (event.type == pygame.MOUSEWHEEL and not pause and start):
            display_info = pygame.display.Info()
            screen_width = display_info.current_w; screen_height = display_info.current_h
            local_map = [list(e) for e in map]
            if (event.y > 0):
                if (nxC > min_xC and nyC > min_yC):
                    for y in range(nyC):
                        # borrar 5 columnas al comienzo 
                        del local_map[y][0:5]
                        # borrar 5 columnas al final
                        del local_map[y][len(local_map[y])-5:]
                    # borrar 3 filas al comienzo
                    del local_map[0:3]
                    # borrar 2 filas al final
                    del local_map[len(local_map)-2:]
                    nxC -= 10; nyC -= 5
                    dimCW = screen_width / nxC; dimCH = screen_height / nyC
                    #for i in local_map:
                        #print(len(i), i)
                    map = local_map
                    #map = [[random.randint(0, 1) for _ in range(nxC)] for _ in range(nyC)]
                else: print("Tamaño mínimo alcanzado.") 
                print("Mouse wheel scrolled up")
            elif (event.y < 0):
                if(nxC < max_xC and nyC < max_yC):
                    nxC += 10; nyC += 5
                    dimCW = screen_width / nxC; dimCH = screen_height / nyC 
                    for y in range(nyC):
                        # añadir 3 filas al comienzo
                        if(y <= 2):
                            local_map.insert(0, [0] * nxC)
                        # añadir 2 filas al final
                        elif(y >= nyC-2):
                            local_map.append([0] * (nxC))

                        for x in range(nxC):
                            # añadir 5 columnas al inicio
                            if(x <= 4 and len(local_map[y]) != nxC):
                                local_map[y].insert(0, 0)
                            # añadir 5 columnas al final
                            if(x >= nxC-5 and len(local_map[y]) != nxC):
                                local_map[y].append(0)
                    #for i in local_map:
                        #print(len(i), i)
                    #map = np.array(local_map)      
                    #print(local_map)
                    map = local_map
                    #map = [[random.randint(0, 1) for _ in range(nxC)] for _ in range(nyC)]
                else: print("Tamaño máximo alcanzado.")
                print("Mouse wheel scrolled down")

                
    clock.tick(120)
    # Update Display Frames     
    pygame.display.update()
                

# Quit game
pygame.quit()