# Multi-Level System Documentation

## Implemented Features

### Level Configuration (3 Levels)

#### Level 1: Introduction
- **Platforms**: 6 platforms with increasing height complexity
- **Fires**: 3 fire hazards positioned on platforms
- **Collectibles**: 4 strawberries to collect
- **Difficulty**: Beginner - moderate platform spacing

#### Level 2: Intermediate
- **Platforms**: 6 platforms with varied heights
- **Fires**: 4 fire hazards (increased from Level 1)
- **Collectibles**: 5 strawberries (increased from Level 1)
- **Difficulty**: Medium - tighter platform spacing, more hazards

#### Level 3: Advanced
- **Platforms**: 8 smaller platforms (0.8x width)
- **Fires**: 6 fire hazards (maximum hazards)
- **Collectibles**: 6 strawberries (maximum collectibles)
- **Difficulty**: Hard - small platforms, many obstacles

### Level Progression
- Players start at Level 1
- Completing a level (collecting all strawberries) shows "Level Complete" menu
- Clicking "Next Level" increments the level counter
- After Level 3, resets to Level 1
- Restarting maintains the current level

### UI Display
The HUD now shows:
1. **Lives**: Red text showing remaining lives (top-left)
2. **Current Level**: Green text showing current level number (below lives)
3. **Fruit Counter**: Yellow text showing collected fruits (below level)

### Game Loop Changes
- `current_level` variable tracks progression (starts at 1)
- `setup_level(level_num)` generates level configurations based on number
- Level increments on "continue" button in Level Complete menu
- `draw()` function updated to accept and display `current_level` parameter

### Code Structure
```python
def setup_level(level_num):
    # Returns: (player, solid_objects, collectibles)
    # Solid objects include floor, platforms, and fires
    # Collectibles are separate for non-collision interaction
```

### Testing Checklist
- [ ] Verify Level 1 loads with 3 fires and 4 strawberries
- [ ] Collect all strawberries and click "Next Level"
- [ ] Verify Level 2 loads with 4 fires and 5 strawberries
- [ ] Verify Level 2 is harder (smaller platforms)
- [ ] Proceed to Level 3 with 6 fires and 6 strawberries
- [ ] Verify Level 3 difficulty (very small platforms)
- [ ] After Level 3, verify wrap-around to Level 1
- [ ] Test restart button maintains level
- [ ] Verify all UI displays correctly (lives, level, fruits)
