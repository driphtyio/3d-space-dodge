#!/usr/bin/env python3
"""
Evolutionary Bot for 3D Space Dodge
====================================
A 6-weight genome evolves a bot that learns to dodge enemies.
See full write-up: https://aigamingdev.com/blog/evolved-bot/
"""
import random, math, json

# ── Game Simulation ──

def simulate(genome, max_time=30.0):
    """Run one episode. Returns survival time in seconds."""
    ARENA = 8.0
    ENEMY_SPEED = 0.04
    SPAWN_INTERVAL = 0.8
    COLLISION_DIST = 1.0
    MAX_ENEMIES = 15

    px, pz = 0.0, 0.0  # player position
    enemies = []
    spawn_timer = 0.0
    t = 0.0
    g = genome[:6]

    while t < max_time:
        t += 1/60.0
        spawn_timer += 1/60.0
        interval = max(0.3, SPAWN_INTERVAL - t * 0.003)

        # Enemy spawning — accelerates over time
        if spawn_timer >= interval and len(enemies) < MAX_ENEMIES:
            spawn_timer = 0
            angle = random.random() * 2 * math.pi
            enemies.append([math.cos(angle) * (ARENA+6), math.sin(angle) * (ARENA+6)])

        # Enemy movement — home toward player, speed up over time
        for i in range(len(enemies)):
            ex, ez = enemies[i]
            dx, dz = px - ex, pz - ez
            dist = math.hypot(dx, dz)
            if dist < COLLISION_DIST:
                return t
            speed = ENEMY_SPEED * (1.0 + t * 0.005)
            enemies[i] = [ex + dx/dist * speed, ez + dz/dist * speed]

        # ── Bot Brain ──
        tg, fs, ws, ca, pd, sc = g
        pd = max(0.5, pd)  # min panic distance
        sc = max(0.05, sc)  # min speed cap

        # Aggregate threat vector from all enemies
        tx, tz, close_d, close_dx, close_dz = 0.0, 0.0, 99.0, 0.0, 0.0
        for ex, ez in enemies:
            dx, dz = px - ex, pz - ez
            d = math.hypot(dx, dz) + 0.01
            w = 1.0 / (d * 0.2 + 0.3)
            tx += dx/d * w
            tz += dz/d * w
            if d < close_d:
                close_d, close_dx, close_dz = d, dx/d, dz/d

        tm = math.hypot(tx, tz) + 0.01
        tx, tz = tx/tm, tz/tm

        # Panic: flee hard when enemies are close
        panic = max(0.0, min(1.0, 1.0 - close_d / pd))

        # Flee direction: away from closest + perpendicular strafe
        flee_x = close_dx * fs + close_dz * 0.4
        flee_z = close_dz * fs - close_dx * 0.4

        # Wander: oscillating random direction
        wander_x = math.sin(t * ws)
        wander_z = math.cos(t * ws * 0.7)

        # Center attraction: don't drift too far
        cx = -px * ca * 0.08
        cz = -pz * ca * 0.08

        # Combine: flee dominates when panicking, wander when safe
        move_x = (flee_x * panic + wander_x * (1-panic) * 0.15 + cx) * tg
        move_z = (flee_z * panic + wander_z * (1-panic) * 0.15 + cz) * tg

        # Speed cap
        speed = math.hypot(move_x, move_z)
        if speed > sc:
            move_x, move_z = move_x/speed*sc, move_z/speed*sc

        px += move_x
        pz += move_z
        px = max(-ARENA, min(ARENA, px))
        pz = max(-ARENA, min(ARENA, pz))

    return max_time


# ── Evolutionary Algorithm ──

def random_genome():
    """Generate a random 6-weight genome."""
    return [random.uniform(0.3, 1.8) for _ in range(6)]

def mutate(genome, rate=0.3, scale=0.25):
    """Mutate a genome with given rate and scale."""
    return [x + random.uniform(-scale, scale) if random.random() < rate else x for x in genome]

def crossover(a, b):
    """Uniform crossover between two parent genomes."""
    return [a[i] if random.random() < 0.5 else b[i] for i in range(len(a))]


def run_evolution(generations=60, pop_size=120, elite=3, max_time=30.0):
    """
    Run the full evolutionary loop.
    
    Args:
        generations: Number of generations
        pop_size: Population size per generation
        elite: Number of top performers to keep unchanged
        max_time: Max simulation time per episode
    
    Returns:
        (best_genome, best_score, history)
    """
    pop = [random_genome() for _ in range(pop_size)]
    best_ever = (None, 0.0)
    history = []

    for gen in range(generations):
        scores = [simulate(ind, max_time) for ind in pop]
        gen_best = max(scores)
        gen_avg = sum(scores) / len(scores)
        history.append({"gen": gen+1, "best": round(gen_best, 1), "avg": round(gen_avg, 1)})

        idx = scores.index(gen_best)
        if gen_best > best_ever[1]:
            best_ever = (pop[idx][:], gen_best)

        if gen_best >= max_time * 0.97:
            break

        # Tournament selection
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        new_pop = [pop[i][:] for i in ranked[:elite]]

        while len(new_pop) < pop_size:
            a = pop[random.choice(ranked[:20])]
            b = pop[random.choice(ranked[:20])]
            child = crossover(a, b)
            child = mutate(child,
                rate=0.3 * (1 - gen/generations) + 0.05,
                scale=0.3 * (1 - gen/generations) + 0.05)
            new_pop.append(child)

        pop = new_pop

    return best_ever[0], best_ever[1], history


# ── Benchmarking ──

def benchmark(genome, label, runs=500):
    """Run many episodes and report statistics."""
    scores = [simulate(genome) for _ in range(runs)]
    avg = sum(scores) / len(scores)
    med = sorted(scores)[len(scores)//2]
    over_20 = sum(1 for s in scores if s >= 20)
    return {
        "label": label,
        "avg": round(avg, 1),
        "median": round(med, 1),
        "survived_20s": over_20,
        "total_runs": runs,
        "pct_over_20s": round(over_20 / runs * 100, 1)
    }


# ── Main ──

if __name__ == "__main__":
    print("=" * 60)
    print("Evolutionary Bot for 3D Space Dodge")
    print("=" * 60)

    # 1. Random baseline
    print("\n[1/3] Establishing random baseline...")
    baseline_scores = [simulate(random_genome()) for _ in range(200)]
    baseline_avg = sum(baseline_scores) / len(baseline_scores)
    baseline_best = max(baseline_scores)
    print(f"  Random bot: avg={baseline_avg:.1f}s  best={baseline_best:.1f}s")

    # 2. Run evolution
    print("\n[2/3] Running evolution...")
    best_genome, best_score, history = run_evolution()

    print(f"\n  Converged in {len(history)} generations")
    print(f"  Best survival: {best_score:.1f}s")
    print(f"  Best genome: {[round(x, 4) for x in best_genome]}")
    print(f"\n  Generations:")
    for h in history:
        marker = " ★" if h["best"] >= 28 else ""
        if h["gen"] % 10 == 1 or marker:
            print(f"    Gen {h['gen']:3d}: best={h['best']:5.1f}s avg={h['avg']:4.1f}s{marker}")

    # 3. Benchmark
    print("\n[3/3] Benchmarking evolved bot vs random...")
    evolved = benchmark(best_genome, "Evolved bot")
    random_b = benchmark(random_genome, "Random movement")

    print(f"\n  {'Metric':20s} {'Random':10s} {'Evolved':10s} {'Improvement':12s}")
    print(f"  {'-'*52}")
    print(f"  {'Average survival':20s} {random_b['avg']:>6.1f}s    {evolved['avg']:>6.1f}s    +{((evolved['avg']-random_b['avg'])/random_b['avg']*100):.0f}%")
    print(f"  {'Median survival':20s} {random_b['median']:>6.1f}s    {evolved['median']:>6.1f}s    +{((evolved['median']-random_b['median'])/random_b['median']*100):.0f}%")
    print(f"  {'Survived 20s+':20s} {random_b['survived_20s']:>6d}/{random_b['total_runs']:<3d}  {evolved['survived_20s']:>6d}/{evolved['total_runs']:<3d}  +{evolved['pct_over_20s']:.0f}pp")

    # 4. Save results
    result = {
        "best_genome": [round(x, 4) for x in best_genome],
        "best_survival_seconds": round(best_score, 1),
        "generations_run": len(history),
        "history": history,
        "benchmark": {"random": random_b, "evolved": evolved},
        "parameters": {
            "arena_radius": 8.0,
            "enemy_speed_base": 0.04,
            "spawn_interval": "0.8s -> 0.3s (accelerates)",
            "max_enemies": 15,
            "collision_distance": 1.0,
            "genome_size": 6,
            "population": 120,
            "max_simulated_time": 30
        },
        "genome_legend": [
            "0: threat_gain — how much enemy proximity affects movement",
            "1: flee_strength — how fast bot flees from closest enemy",
            "2: wander_speed — oscillation frequency of wander direction",
            "3: center_attract — how strongly bot stays near arena center",
            "4: panic_distance — distance at which bot starts panicking",
            "5: speed_cap — maximum movement speed"
        ]
    }

    with open("evolution-results.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n  Results saved to evolution-results.json")
    print("\n" + "=" * 60)
    print("Done.")
