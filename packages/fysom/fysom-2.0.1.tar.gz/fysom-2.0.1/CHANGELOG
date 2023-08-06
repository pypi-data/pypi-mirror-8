Changelog for fysom
--------------------
* v2.0.1
  State re-entry or 'reflexive' callbacks (onreenter_state) called when the start and end state of a transition
  are the same. This is different to the change in v1.1.0 as the new callback type is for a particular state and not
  a particular event. This allows individual callbacks for reflexive transitions rather than event callbacks
  with conditional branches to handle both reflexive and non-reflexive transitions.
  Pull request by [@mattjml](https://github.com/mattjml)

* v2.0.0
  BREAKING CHANGE - Canceling an event by returning `False` from the onbefore<event> callback
  will now raise `fysom.Canceled` instead of just ignoring the event.

* v1.1.2
  Extend Fysom constructor to allow for terser FSM specifications. Pull request by [@astanin](https://github.com/astanin).

* v1.1.1
  Resolved problems with installation on windows.

* v1.1.0
  Event callbacks (onbefore_event_|onafter_event_|on_event_) will now trigger
  when the state does not change.
  Previously those callbacks would only fire in the case of a state change,
  so events keeping the FSM in the same state would not fire callbacks at all.

* v1.0.19
  The `trigger` method now accepts any positional arguments and keyword arguments, and passes them to the underlying event method. Pull request by 
  [@poundifdef](https://github.com/poundifdef).

* v1.0.18
  From now on, a changelog will be included. Furthermore, all PyPI releases will be GPG signed.
