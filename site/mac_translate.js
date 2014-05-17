var translations = {

}

function translate_mac(mac, current_host_name) {
    if ( mac in translations ) return translations[mac];
    return current_host_name
}