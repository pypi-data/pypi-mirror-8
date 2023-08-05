# Copyright (C) 1997-2014 Sam Lantinga <slouken@libsdl.org>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely.

# Python translation by Daniel Holth <dholth@fastmail.fm>, 2014

import math
import sys
import sdl

SHAPED_WINDOW_X	= 150
SHAPED_WINDOW_Y	= 150
SHAPED_WINDOW_DIMENSION	= 640

class LoadedPicture:
    pass

# typedef struct LoadedPicture {
#     SDL_Surface *surface
#     SDL_Texture *texture
#     SDL_WindowShapeMode mode
#     const name LoadedPicture

def render(renderer, texture, texture_dimensions):
    # Clear render-target to blue.
    sdl.setRenderDrawColor(renderer,0x00,0x00,0xff,0xff)
    sdl.renderClear(renderer)

    # Render the texture.
    SDL_RenderCopy(renderer,texture,&texture_dimensions,&texture_dimensions)

    SDL_RenderPresent(renderer)

def main(argc,argv):
    Uint8 num_pictures
    LoadedPicture* pictures
    SDL_PixelFormat* format = NULL
    SDL_Window *window
    SDL_Renderer *renderer
    SDL_Color black = {0,0,0,0xff}
    SDL_Event event
    event_pending = 0
    should_exit = 0
    unsigned current_picture
    Uint32 pixelFormat = 0
    access = 0
    SDL_Rect texture_dimensions

    # Enable standard application logging
    SDL_LogSetPriority(SDL_LOG_CATEGORY_APPLICATION, SDL_LOG_PRIORITY_INFO)

    if argc < 2:
		SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_Shape requires at least one bitmap file as argument.")
        os.exit(-1)

    if SDL_VideoInit(NULL) == -1:
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Could not initialize SDL video.")
        os.exit(-2)

    num_pictures = argc - 1
    pictures = (LoadedPicture *)SDL_malloc(sizeof(LoadedPicture)*num_pictures)
    for(i=0;i<num_pictures;i++)
        pictures[i].surface = NULL
    for(i=0;i<num_pictures;i++) {
        pictures[i].surface = SDL_LoadBMP(argv[i+1])
        pictures[i].name = argv[i+1]
        if pictures[i].surface == NULL:
            j = 0
            for(j=0;j<num_pictures;j++)
                SDL_FreeSurface(pictures[j].surface)
            SDL_free(pictures)
            SDL_VideoQuit()
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Could not load surface from named bitmap file: %s" % (argv[i+1]))
            os.exit(-3)

        format = pictures[i].surface.format
        if SDL_ISPIXELFORMAT_ALPHA(format.format):
            pictures[i].mode.mode = ShapeModeBinarizeAlpha
            pictures[i].mode.parameters.binarizationCutoff = 255
        else:
            pictures[i].mode.mode = ShapeModeColorKey
            pictures[i].mode.parameters.colorKey = black

    window = SDL_CreateShapedWindow("SDL_Shape test",
        SHAPED_WINDOW_X, SHAPED_WINDOW_Y,
        SHAPED_WINDOW_DIMENSION,SHAPED_WINDOW_DIMENSION,
        0)
    SDL_SetWindowPosition(window, SHAPED_WINDOW_X, SHAPED_WINDOW_Y)
    if window == NULL:
        for(i=0;i<num_pictures;i++)
            SDL_FreeSurface(pictures[i].surface)
        SDL_free(pictures)
        SDL_VideoQuit()
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Could not create shaped window for SDL_Shape.")
        os.exit(-4)
    renderer = SDL_CreateRenderer(window,-1,0)
    if not renderer:
        SDL_DestroyWindow(window)
        for(i=0;i<num_pictures;i++)
            SDL_FreeSurface(pictures[i].surface)
        SDL_free(pictures)
        SDL_VideoQuit()
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Could not create rendering context for SDL_Shape window.")
        os.exit(-5)

    for(i=0;i<num_pictures;i++)
        pictures[i].texture = NULL
    for(i=0;i<num_pictures;i++) {
        pictures[i].texture = SDL_CreateTextureFromSurface(renderer,pictures[i].surface)
        if pictures[i].texture == NULL:
            j = 0
            for(j=0;j<num_pictures;i++)
                if pictures[i].texture != NULL:
                    SDL_DestroyTexture(pictures[i].texture)
            for(i=0;i<num_pictures;i++)
                SDL_FreeSurface(pictures[i].surface)
            SDL_free(pictures)
            SDL_DestroyRenderer(renderer)
            SDL_DestroyWindow(window)
            SDL_VideoQuit()
            SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Could not create texture for SDL_shape.")
            os.exit(-6)

    event_pending = 0
    should_exit = 0
    event_pending = SDL_PollEvent(&event)
    current_picture = 0
    button_down = 0
    texture_dimensions.h = 0
    texture_dimensions.w = 0
    texture_dimensions.x = 0
    texture_dimensions.y = 0
    SDL_LogInfo(SDL_LOG_CATEGORY_APPLICATION, "Changing to shaped bmp: %s" % (pictures[current_picture].name))
    SDL_QueryTexture(pictures[current_picture].texture,(Uint32 *)&pixelFormat,()&access,&texture_dimensions.w,&texture_dimensions.h)
    SDL_SetWindowSize(window,texture_dimensions.w,texture_dimensions.h)
    SDL_SetWindowShape(window,pictures[current_picture].surface,&pictures[current_picture].mode)
    while should_exit == 0:
        event_pending = SDL_PollEvent(&event)
        if event_pending == 1:
            if event.type == SDL_KEYDOWN:
                button_down = 1
                if event.key.keysym.sym == SDLK_ESCAPE:
                    should_exit = 1
                    break
            if button_down and event.type == SDL_KEYUP:
                button_down = 0
                current_picture += 1
                if current_picture >= num_pictures:
                    current_picture = 0
                SDL_LogInfo(SDL_LOG_CATEGORY_APPLICATION, "Changing to shaped bmp: %s" % (pictures[current_picture].name))
                SDL_QueryTexture(pictures[current_picture].texture,(Uint32 *)&pixelFormat,()&access,&texture_dimensions.w,&texture_dimensions.h)
                SDL_SetWindowSize(window,texture_dimensions.w,texture_dimensions.h)
                SDL_SetWindowShape(window,pictures[current_picture].surface,&pictures[current_picture].mode)
            if event.type == SDL_QUIT:
                should_exit = 1
            event_pending = 0
        render(renderer,pictures[current_picture].texture,texture_dimensions)
        SDL_Delay(10)

    # Free the textures.
    for(i=0;i<num_pictures;i++)
        SDL_DestroyTexture(pictures[i].texture)
    SDL_DestroyRenderer(renderer)
    # Destroy the window.
    SDL_DestroyWindow(window)
    # Free the original surfaces backing the textures.
    for(i=0;i<num_pictures;i++)
        SDL_FreeSurface(pictures[i].surface)
    SDL_free(pictures)
    # Call SDL_VideoQuit() before quitting.
    SDL_VideoQuit()

    return 0

# vi: set ts=4 sw=4 expandtab:
