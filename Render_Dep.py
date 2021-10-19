from RayCast import RayCast
MAX_DEPTH = 10


def Render(wnd, cam, map): 
    """
    Draws to the terminal with the distance from the camera to the wall
    """
    wnd.Refresh()
    for x in range(wnd.width):
        raycast = RayCast(cam.posX, cam.posY,                                   # send a ray, from player position
                            cam.dirX + cam.planeX * (2 * x / wnd.width - 1),   # rotate ray relative to the middle of the screen
                            cam.dirY + cam.planeY * (2 * x / wnd.width - 1))

        while True:
            mapvalue = map[raycast.Step()]          # iterate raycast along line
            if (mapvalue > 0):                      # if collision with wall
                raydepth = raycast.IntersectDepth() # get intersect data
                break                               

        lineheight = int(wnd.height / raydepth)                             # line height relative to the screens height
        start = int(wnd.height // 2 - lineheight * (cam.posZ))              # start = middle minus half line height
        end = 	int(wnd.height // 2 + lineheight * (1 - cam.posZ))          # end   = middle plus half line height
        colour = 232 + int(24 * max(0, min(1 - (raydepth / MAX_DEPTH), 1))) # gradient from 0-24
        
        for y in range(max(start, 0), min(end, wnd.height - 1)):
            wnd.SetPixel(x, y, colour)