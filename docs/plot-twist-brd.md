# Plot Twist — business requirements (summary)

Source: https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/weeks/week-05/01-plot-twist-brd.html

## Concept

A short, original mystery or escape room (about ten minutes of play). The player explores through meaningful choices; finding clues or making decisions changes what is possible. Text and simple controls are required; images and sound are optional.

## Content baseline

- **Scenes:** at least five. The opening scene starts the game.
- **Items:** at least two. Each is collectible only where the story makes it available, once per game. At least one item unlocks an action. Items are reusable (using one does not consume it).
- **Endings:** two reachable endings, clearly identified. One depends on an earlier choice or item. Once reached, story actions stop; the player can review the outcome or start a new game.

## Business rules

- **R1** An action is allowed only when its scene and prerequisites are met. A blocked action does not move the player or change the inventory.
- **R2** Items are collected only where the story makes them available, once per game, and are reusable.
- **R3** Visited scenes reflect remembered changes (a taken key is not offered again).
- **R4** A new game resets all progress but keeps the story content. Every ending is reachable through valid play from a new game.

## Requirements

- **PT01 Start and resume** — new game, and resume if a save exists. Restarting asks for confirmation before replacing progress.
- **PT02 Explore** — show the current scene and its actions. Every accepted choice produces a visible result.
- **PT03 Collect and use** — the player can inspect the inventory. Collecting an item twice creates no duplicate.
- **PT04 Apply consequences** — at least one remembered decision affects a later action or ending. Blocked actions are explained or hidden until their conditions are met.
- **PT05 Finish and replay** — endings are clearly identified; the player can replay from the start.

## Acceptance scenarios

- **A1 Locked route** — without the key, the locked route is unavailable or rejected; scene and inventory unchanged.
- **A2 Unlocked route** — with the key, the route leads to the intended scene and the key stays in the inventory.
- **A3 No duplicate collection** — collecting an item again leaves one copy.
- **A4 Resume** — after collecting an item and making a consequential choice, reopening the app restores the scene, item and choice; routes stay available.
- **A5 Two outcomes** — two valid paths from separate new games reach different endings. Story actions cannot change a completed game.
- **A6 Restart safely** — cancelling a restart keeps progress; confirming restores the opening scene, empty inventory and initial decisions.

## Persistence

- Store the story content: scenes, choices, item locations and conditions.
- For the active game store: current scene, collected items, relevant decisions, and whether an ending was reached.
- Save after each accepted action. Rejected actions leave saved data unchanged. Accepted changes survive an app restart.

## Out of scope (first release)

Visual story editor, procedural generation, multiplayer, combat, live AI dialogue, paid or live external services.

## Future extensions (suggested for the team project)

A story editor or additional mysteries.
