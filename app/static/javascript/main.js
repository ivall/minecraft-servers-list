toastr.options = {
	"closeButton": true,
	"debug": false,
	"newestOnTop": true,
	"progressBar": true,
	"positionClass": "toast-top-right",
	"preventDuplicates": true,
	"onclick": null,
	"showDuration": "300",
	"hideDuration": "1000",
	"timeOut": "5000",
	"extendedTimeOut": "1000",
	"showEasing": "swing",
	"hideEasing": "linear",
	"showMethod": "fadeIn",
	"hideMethod": "fadeOut"
};
$(document).on("click", ".td-ip", function () {
	var ip = $(this);
	var $temp = $("<input>");
	$("body").append($temp);
	$temp.val($(ip).html()).select();
	document.execCommand("copy");
	$temp.remove();
	toastr.success("Skopiowano ip: "+ip.text());
});
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});