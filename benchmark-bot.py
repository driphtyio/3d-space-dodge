#!/usr/bin/env python3
"""Visualize the evolved bot vs random baseline."""
import json, random, math, subprocess, sys

with open('/tmp/evolution-results.json') as f:
    data = json.load(f)

best = data['best_genome']

def trial(genome, label, runs=500):
    """Run many episodes and report stats."""
    scores = []
    ARENA, SPEED, INTERVAL, COLLIDE = 8.0, 0.04, 0.8, 1.0
    
    for _ in range(runs):
        px, pz, enemies, spawn_timer, t = 0.0, 0.0, [], 0.0, 0.0
        
        while t < 30:
            t += 1/60.0
            spawn_timer += 1/60.0
            interval = max(0.3, INTERVAL - t * 0.003)
            
            if spawn_timer >= interval:
                spawn_timer = 0
                a = random.random() * 2 * math.pi
                enemies.append([math.cos(a) * (ARENA+6), math.sin(a) * (ARENA+6)])
            
            for i in range(len(enemies)):
                ex, ez = enemies[i]
                dx, dz = px - ex, pz - ez
                dist = math.hypot(dx, dz)
                if dist < COLLIDE:
                    scores.append(t)
                    t = 999
                    break
                s = SPEED * (1.0 + t * 0.005)
                enemies[i] = [ex + dx/dist * s, ez + dz/dist * s]
            
            if t > 100: break
            
            if genome:
                tg, fs, ws, ca, pd, sc = genome
                pd, sc = max(0.5, pd), max(0.05, sc)
                tx, tz, cd, cdx, cdz = 0.0, 0.0, 99.0, 0.0, 0.0
                for ex, ez in enemies:
                    dx, dz = px - ex, pz - ez
                    d = math.hypot(dx, dz) + 0.01
                    w = 1.0 / (d * 0.2 + 0.3)
                    tx += dx/d * w
                    tz += dz/d * w
                    if d < cd: cd, cdx, cdz = d, dx/d, dz/d
                tm = math.hypot(tx, tz) + 0.01
                tx, tz = tx/tm, tz/tm
                panic = max(0.0, min(1.0, 1.0 - cd / pd))
                flee_x = cdx * fs + cdz * 0.4
                flee_z = cdz * fs - cdx * 0.4
                wander_x = math.sin(t * ws)
                wander_z = math.cos(t * ws * 0.7)
                mx = (flee_x * panic + wander_x * (1-panic) * 0.15 + -px * ca * 0.08) * tg
                mz = (flee_z * panic + wander_z * (1-panic) * 0.15 + -pz * ca * 0.08) * tg
                ms = math.hypot(mx, mz)
                if ms > sc: mx, mz = mx/ms*sc, mz/ms*sc
                px += mx
                pz += mz
                px = max(-ARENA, min(ARENA, px))
                pz = max(-ARENA, min(ARENA, pz))
            else:
                # Random baseline
                px += random.uniform(-0.15, 0.15)
                pz += random.uniform(-0.15, 0.15)
                px = max(-ARENA, min(ARENA, px))
                pz = max(-ARENA, min(ARENA, pz))
        
        if t < 100:
            scores.append(t)
    
    avg = sum(scores) / len(scores)
    med = sorted(scores)[len(scores)//2]
    over_20 = sum(1 for s in scores if s >= 20)
    print(f"  {label:25s}: avg={avg:.1f}s median={med:.1f}s survived_20s={over_20}/{runs} ({over_20/runs*100:.0f}%)")

print("Benchmark Results (30s max, 500 runs each)")
print()
trial(None, "Random movement")
trial(best, "Evolved bot")
