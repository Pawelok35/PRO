def calculate_power_rating_interactive(team_data: dict) -> float:
    """
    Interactively lets user choose which factors to include in Power Rating.
    Returns the calculated Power Rating.
    """
    all_components = {
        "xPTS_avg": 0.27,
        "xG_diff": 0.18,
        "form_score": 0.13,
        "dominance_ratio": 0.10,
        "SoS_factor": 0.12,
        "momentum": 0.10,
        "efficiency_vs_opponent_tier": 0.10
    }

    print("\n📊 Available Power Rating components:")
    for i, (key, weight) in enumerate(all_components.items(), 1):
        print(f"{i}. {key} (weight: {weight})")

    selected_indices = input(
        "\nEnter numbers of components to include (comma-separated, e.g. 1,3,5): "
    )
    
    try:
        selected_keys = [
            list(all_components.keys())[int(i.strip()) - 1]
            for i in selected_indices.split(",")
        ]
    except Exception:
        print("❌ Invalid input. Using all components by default.")
        selected_keys = list(all_components.keys())

    rating = 0.0
    for key in selected_keys:
        weight = all_components[key]
        value = team_data.get(key, 0)
        rating += value * weight

    print(f"\n✅ Included components: {selected_keys}")
    return round(rating, 3)
