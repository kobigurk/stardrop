const axios = require("axios");
const fs = require("fs");

async function main() {
	var humanList = [];
	let graphQuery = "{submissions(first:1000){id creationTime submissionTime status registered name vouchees{id} requests{evidence{sender URI}}}}";
	let graphData;
    
    let id = 0;
        let count = 0;
        let limit = 8000;
        let data = {"submissions":[]};

        while(count <= limit){
            let query = '{submissions(first: 1000, where: {id_gt:"'+id+'"}){id creationTime submissionTime status registered name vouchees{id} requests{evidence{sender URI}}}}';
            console.log(query);
            let response = await axios.post("https://api.thegraph.com/subgraphs/name/kleros/proof-of-humanity-mainnet", {query: query})
                .then((res)=>{
                    console.log(res.data);
                    return res;
                })
                .catch((error)=>{
                    console.log(error);
                    return false;
                })
            if(!response){count = limit+1; return false;}

            for (var i = 0; i < response.data.data.submissions.length; i++) {
               data["submissions"].push(response.data.data.submissions[i]);
            }
            count+=1000;
            id = String(response.data.data.submissions[response.data.data.submissions.length - 1].id);
            // console.log("next i ", i);
            // console.log("next count ", count);
        }
        graphData = {"data": data};

data.submissions.forEach((human) => {
	humanList.push(human.id)
});

fs.writeFileSync("./humanList.json", JSON.stringify(humanList));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
