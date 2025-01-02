db = connect("mongodb://localhost:27017/ski_planner");

// Insert initial data
db.users.insertMany([
  { username: "nice_user", friends: ["Marie", "Carl"], equipment: {ski: "rossignol"} }
]);

// This is the admin user, currently the password is set to admin/admin but it must be changed for production
db.power_users.insertMany([
    { username: "admin", hashed_password: "$argon2id$v=19$m=65536,t=3,p=4$y9l7r7XW2jtnrJWyFsLYOw$JgOjn0y0lXg8MAbcj5ckfzDrn7CgrRE5aygwd8els8s", disabled: false }
])