- handle shutdown much cleaner, ie. exceptions:
  - KeyboardInterrupt
  - etc.

- move /media/rpi-data/raspi-door => /local/raspi-door & autoload

- give temperature text colors in a range from cold(blue) to hot(red)

- make ^C interrupt raspi-door even if no GUI events are triggered...

- make a "Lock" object that has:
    - current state
    - next state => if not-null, transitioning
    - requested state

    - states can be:
        - unlocked
        - locked
        - permalocked

- if Lock.next != NULL, disable buttons?
  => NO. just update `Lock.requested`

- hide the mouse pointer in wx...

- for camera.capture, determine the most efficient 'format'
  parameter...

- there's a lot of duplication in the yahoo weather icons... dedup!

- convert everything to `logging` based output
