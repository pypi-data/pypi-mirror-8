class HeaderCtrl extends Ctrl
    gatherElements: ->
        @elements =
            menu: @element.find('nav')
            main: @element.find('.main')
            learn: @element.find('.learn-more')
            gettingStartedAnchor: $('.getting-started-anchor')
            gettingStarted: @element.find('.learn-more')
            burger: $('.burger')
            contents: $('.contents')
            body: $('body')
            mobileNav: $('.mobile-nav')

        @isLocked = false
        @top = 120
        @bottom = @elements.main.offset().top
        @opaqueMin = @element.height() - @elements.menu.height()
        @gettingStartedAnchorTop = @elements.gettingStartedAnchor.offset().top
        @anchorOffset = 120

    bindEvents: ->
        $(document).scrollspy
            onTick: (element, position, inside, enters, leaves) =>
                if position.top < @top
                    @elements.main.css('opacity', 100)
                    @elements.learn.css('opacity', 100)
                    return

                opacity = (@bottom - position.top) / (@bottom - @top)
                @elements.main.css('opacity', opacity)
                @elements.learn.css('opacity', opacity)

        @elements.gettingStarted.on('click', (ev) =>
            $('html, body').animate(
                scrollTop: @gettingStartedAnchorTop - @anchorOffset
            , 1000)
        )

        @elements.menu.scrollspy
            min: 15
            max: 10000000000
            onEnter: (element, position) =>
                @elements.menu.addClass('static')
            onLeave: (element, position) =>
                @elements.menu.removeClass('static')
        .scrollspy
            min: @opaqueMin
            max: 10000000000
            onEnter: (element, position) =>
                @elements.menu.addClass('opaque')
            onLeave: (element, position) =>
                @elements.menu.removeClass('opaque')

        @elements.contents.on('click', (ev) =>
            @toggleNavigation() if @isLocked
        )

        @elements.burger.on('click', (ev) =>
            ev.preventDefault()
            ev.stopPropagation()
            @toggleNavigation()
        )

    toggleNavigation: ->
        @elements.contents.toggleClass('hidden')
        @elements.mobileNav.toggleClass('visible')

        if @isLocked
            setTimeout(=>
                @elements.body.toggleClass('locked')
            , 300
            )
        else
            @elements.body.toggleClass('locked')

        @isLocked = not @isLocked
