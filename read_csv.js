var csv = require("fast-csv");

csv
.fromPath("pro_users_concurrent.csv", {headers: ["user", "domain", "username", "password"]})
.on("data", function(user){
  console.log(user);
})
.on("end", function(){
  console.log("done");
});