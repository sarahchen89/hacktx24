import React, { useEffect, useState } from 'react';
import { useRouter } from 'expo-router';

interface UserProfile {
  first_name: string;
  last_name: string;
  email: string;
  username: string;
}

const Profile: React.FC = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Fetch user profile data
    const fetchUserData = async () => {
      const username = localStorage.getItem('username'); // Assumes username is stored on login
      if (username) {
        try {
          const response = await fetch(`/api/users/${username}`);
          if (!response.ok) {
            throw new Error('Failed to fetch user data');
          }
          const data = await response.json();
          setUser(data.user);
        } catch (error) {
          console.error('Error fetching user data:', error);
        }
      } else {
        router.back(); // Redirect if no username is stored
      }
    };

    fetchUserData();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('username'); // Clear stored user info
    router.replace('/signin'); // Redirect to sign-in page
  };

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="profile">
      <h2>User Profile</h2>
      <div>
        <strong>First Name:</strong> {user.first_name}
      </div>
      <div>
        <strong>Last Name:</strong> {user.last_name}
      </div>
      <div>
        <strong>Email:</strong> {user.email}
      </div>
      <div>
        <strong>Username:</strong> {user.username}
      </div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Profile;