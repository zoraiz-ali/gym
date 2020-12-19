from gym_robot.envs.robot_env import RobotEnv


def run(env, nr_games=100, render=True, fps=None):
    """
        Run an environment.

        :param env:
            This is either the gym environment or the
            direct robot environment.
        :param int nr_games:
            Number of episodes that are going to be run.
        :param bool render:
            If True will render the game in a small window.
        :param Union[None, int] fps:
            Frame rate of the game, when None is provided the
            game will go as fast as possible. This will only
            have effect when rendering is set to True.
    """

    for episode in range(1, nr_games + 1):
        env.reset()
        done = False
        score = 0
        frames = 0
        while not done:
            obs, reward, done, info = env.step(env.action_space.sample())
            if render: env.render(delay=(1000 / fps) if fps is not None else 1)
            score += reward
            frames += 1
            print(f"\r\tRunning episode: {episode:4d}, steps: {frames:5d}, score: {score: 5d}", end='')
        print(f"\rFinished episode {episode:4d} in {frames:5d} steps, with a score of {score: 5d}")
    print(f"Finished run", end="\n\n")


if __name__ == '__main__':
    import gym

    # Run the environment from gym
    env = gym.make('robot-v0')
    run(env, nr_games=100, render=True, fps=None)

    # Run the environment without gym
    env = RobotEnv()
    run(env, nr_games=100, render=True, fps=None)
