



//alert("table 2.js has been loaded");

$(document).ready( function () {
    $('#wholeTable').DataTable(
      {
          "pagingType": "simple",
          "paging": true,
          "pageLength": 100,
          "searchPlaceholder": "Filter by keyword",
          "order": [],
          language: {
        search: "Filter the outcomes   ",
        searchPlaceholder: "keyword (e.g. hospitalization)    ",
         "paginate": {
      "next": "   -Next-  ",
      "previous": "  -Previous-  "
    }
    }
        
      });

})




      
  $('.restNCTs').hide();


  $('.showMoreLink').click(function() {
  $(this).prev().prev().slideToggle("fast");
  $(this).prev().slideToggle("fast");
 if($(this).text()=="show more") {
     $(this).text("show less");
     $(this).addClass("clickedShowMore");
  }
  else{
     $(this).text("show more");
  }
 
  //$('.dots').prev().hide(); 

});



function filter() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("filterVal");
  filter = input.value.toLowerCase();
  table = document.getElementById("outcomeTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toLowerCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}


function showAllNCTs(outcomeName, links) {
  //doesnt work
  var text = "showAllNCTs function called. Outcome ";
  alert(outcomeName);
  var outDots = document.getElementById(outcomeName+"dots");
  console.log("Value of dots: ", outDots.innerHTML);
  outDots.innerHTML = links.join(" - ");
  console.log("Value of dots after change: ", outDots.innerHTML);
  showMoreLink = document.getElementById(outcomeName+"showMore");
  showMoreLink.innerHTML = "SHOW LESS";
}
