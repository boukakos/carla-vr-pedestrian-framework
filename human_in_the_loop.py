import carla
import random
import time
import math

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    vehicle_list = []
    walker_list = []

    try:
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        spawn_points = world.get_map().get_spawn_points()

        # ---------------------------------------------------
        # 1. Ρύθμιση Traffic Manager (Αποφυγή Πεζών)
        # ---------------------------------------------------
        tm = client.get_trafficmanager(8000)
        tm_port = tm.get_port()
        tm.set_global_distance_to_leading_vehicle(4.0)

        # ---------------------------------------------------
        # 2. Spawn 40 Αυτόνομων Οχημάτων
        # ---------------------------------------------------
        print("Γίνεται spawn σε 40 αυτόνομα οχήματα...")
        vehicle_bps = blueprint_library.filter('vehicle.*')
        random.shuffle(spawn_points)

        for i in range(min(20, len(spawn_points))):
            bp = random.choice(vehicle_bps)
            vehicle = world.try_spawn_actor(bp, spawn_points[i])
            if vehicle is not None:
                vehicle.set_autopilot(True, tm_port)
                tm.ignore_walkers_percentage(vehicle, 0)
                tm.auto_lane_change(vehicle, False)
                tm.vehicle_percentage_speed_difference(vehicle, -25)
                tm.distance_to_leading_vehicle(vehicle, 4.5)
                vehicle_list.append(vehicle)

        print(f"Στο χάρτη κινούνται {len(vehicle_list)} οχήματα.")

        # ---------------------------------------------------
        # 3. Spawn CARLA Walker (Κλώνος σε ασφαλές σημείο)
        # ---------------------------------------------------
        walker_bp = blueprint_library.find('walker.pedestrian.0001')
        if walker_bp.has_attribute('is_invincible'):
            walker_bp.set_attribute('is_invincible', 'true')

        initial_sp = spawn_points[-1]
        initial_sp.location.z += 0.5
        clone = world.try_spawn_actor(walker_bp, initial_sp)

        if clone is None:
            clone = world.spawn_actor(walker_bp, initial_sp)

        walker_list.append(clone)
        print(f"Ο κλώνος είναι ενεργός (ID: {clone.id}).")

        # ---------------------------------------------------
        # 4. Βρόχος Συγχρονισμού με Ασφαλή Απόσταση
        # ---------------------------------------------------
        spectator = world.get_spectator()
        print("Η προσομοίωση τρέχει! Περπάτα στον δρόμο. (Ctrl+C για έξοδο)")

        MIN_SAFE_DISTANCE = 1.6  # ελάχιστη απόσταση clone-παίκτη σε μέτρα

        while True:
            world.wait_for_tick()
            cam_tf = spectator.get_transform()
            player_loc = cam_tf.location

            yaw_rad = math.radians(cam_tf.rotation.yaw)
            forward_x = math.cos(yaw_rad) * MIN_SAFE_DISTANCE
            forward_y = math.sin(yaw_rad) * MIN_SAFE_DISTANCE

            target_loc = carla.Location(
                x=player_loc.x + forward_x,
                y=player_loc.y + forward_y,
                z=player_loc.z - 0.85
            )

            clone.set_transform(carla.Transform(target_loc, cam_tf.rotation))

    except KeyboardInterrupt:
        print("\nΖητήθηκε τερματισμός από τον χρήστη...")

    finally:
        print("Καθαρισμός οχημάτων και κλώνου...")
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])
        client.apply_batch([carla.command.DestroyActor(x) for x in walker_list])
        print("Ολοκληρώθηκε.")

if __name__ == '__main__':
    main()

