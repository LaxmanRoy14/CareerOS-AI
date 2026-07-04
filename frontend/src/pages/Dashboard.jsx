import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { user } = useAuth();
  const { logout } = useAuth();

  return (
    <div>
      <h1>Dashboard</h1>

      <button
        onClick={() => {
          logout();

          window.location.href = "/login";
        }}
      >
        Logout
      </button>

      <h2>Welcome {user?.full_name}</h2>

      <p>{user?.email}</p>
    </div>
  );
}

export default Dashboard;
