from typing import List
from skanym.core.animate import JointAnimation


class Animation:
    """Class to represent an animation. Contains a list of all joint animations for a given animation.

    Attributes:
    ----------
    joint_animations : (JointAnimation) list
        The joint animations that make up the animation.
    max_key_time : float
        The maximum time value of any key in the animation.
        Is indicative of the duration of the animation.
    """

    def __init__(self, joint_animations: List[JointAnimation] = [], max_key_time=1.0):
        """**Default constructor for the Animation class.**

        Parameters:
        ----------
        joint_animations : (JointAnimation) list, optional
            The joint animations that make up the animation, by default empty list.
        max_key_time : float, optional
            The max_time of the animation. By default, 1.0.
        """
        self.joint_animations = joint_animations
        self.max_key_time = max_key_time

    def compute_max_key_time(self):
        """Computes the maximum time value of any key in the animation.

        Note
        ----------
        Animations loaded with the load_fbx method in skanym/utils/loader.py have a max_key_time already computed.
        """
        max_key_time = 1.0
        for joint_animation in self.joint_animations:
            max_translation_time = joint_animation.translation_curve.get_max_key_time()
            max_rotation_time = joint_animation.rotation_curve.get_max_key_time()
            max_key_time = max(max_key_time, max_translation_time, max_rotation_time)
        self.max_key_time = max_key_time

    def get_joint_animation_by_name(self, joint_name: str):
        """
        Returns the joint animation with the given name.

        Parameters:
        ----------
        joint_name : str
            The name of the joint animation to return.

        Raises:
        ----------
        ValueError
            If no joint animation with the given name is found.
        
        Returns:
        ----------
        JointAnimation
            The joint animation with the given name.
        """
        for joint_animation in self.joint_animations:
            if joint_animation.joint_name == joint_name:
                return joint_animation
        raise ValueError(f"No joint animation with name {joint_name}.")


    def remove_joint_animation_with_no_joint(self):
        """
        Removes all joint animations with no joint.
        """
        self.joint_animations = [joint_animation for joint_animation in self.joint_animations if joint_animation.joint is not None]


    def shift_animation(self, time_shift: float):
        """
        Shifts the animation by the given time shift.

        Parameters:
        ----------
        time_shift : float
            The time shift to apply to the animation.
        """
        for joint_animation in self.joint_animations:
            joint_animation.shift_curves(time_shift)

    def __repr__(self):
        return f"Animation(joint_animations={str(self.joint_animations)}, max_key_time={str(self.max_key_time)}"
