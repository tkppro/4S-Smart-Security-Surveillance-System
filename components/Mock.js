const mockData = [
    {
        id: 1,
        personName: "Unknown",
        image: require("../assets/images/dataset/download.png"),
        detectedAt: "2020-05-10",
        visibleTime: "3 mins",
        markAsSeen: true,
        note: "Detect knife"            
    },
    {
        id: 2,
        personName: "Thang",
        image: require("../assets/images/dataset/download.png"),
        detectedAt: "2020-04-12 8:00",  
        visibleTime: "3 mins",
        markAsSeen: false,
        note: "Detect phone"              
    },
    {
        id: 3,
        personName: "Mom",
        image: require("../assets/images/dataset/download.png"),
        detectedAt: "2020-05-12 8:00", 
        visibleTime: "2 mins",
        markAsSeen: false,
        note: "Nothing"               
    },
    {
        id: 4,
        personName: "Unknown",
        image: require("../assets/images/dataset/download.png"),
        detectedAt: "2020-04-03 8:00",   
        visibleTime: "2 mins",
        markAsSeen: false,
        note: "Nothing"             
    },
];

export default mockData;