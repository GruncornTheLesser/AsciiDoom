from RayCast import RayCast


MAX_DEPTH = 8

def Render(wnd, cam, map):
    """Draws scene to the terminal"""
    for x in range(wnd.width):
        raycast = RayCast(cam.posX, cam.posY,                                   # send a ray, from player position
                            cam.dirX + cam.planeX * (2 * x / wnd.width - 1),   # rotate ray relative to the middle of the screen
                            cam.dirY + cam.planeY * (2 * x / wnd.width - 1))
        while True:
            mapvalue = map[raycast.Step()]                  # iterate raycast along line
            if (mapvalue > 0):                              # if collision with wall
                raydepth, tex_u = raycast.IntersectData()   # get intersect data
                break

        lineheight = int(wnd.height / raydepth)                    # line height relative to the screens height
        start = int(wnd.height // 2 - lineheight * (cam.posZ))     # start = middle minus half line height
        end = 	int(wnd.height // 2 + lineheight * (1 - cam.posZ)) # end   = middle plus half line height
        raydepth = (raydepth / MAX_DEPTH)                          # normalized raydepth 0-1
    
        for y in range(max(start, 0), min(end, wnd.height - 1)): # clamps range
            colour = wnd.Textures[mapvalue - 1].get_Pixel(lineheight, tex_u, (y - start) / lineheight)
            wnd.SetPixel(x, y, colour)

    return wnd.Refresh()


