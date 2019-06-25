L.controlCredits=function(t){return new L.CreditsControl(t)},L.CreditsControl=L.Control.extend({options:{position:"bottomright"},initialize:function(t){if(!t.text)throw"L.CreditsControl missing required option: text";if(!t.image)throw"L.CreditsControl missing required option: image";if(!t.link)throw"L.CreditsControl missing required option: link";L.setOptions(this,t)},onAdd:function(t){this._map=t;var i=L.DomUtil.create("div","leaflet-credits-control",i);i.style.backgroundImage="url("+this.options.image+")",this.options.width&&(i.style.paddingRight=this.options.width+"px"),this.options.height&&(i.style.height=this.options.height+"px");var o=L.DomUtil.create("a","",i);return o.target="_blank",o.href=this.options.link,o.innerHTML=this.options.text,i.link=o,L.DomEvent.addListener(i,"mousedown",L.DomEvent.stopPropagation).addListener(i,"click",L.DomEvent.stopPropagation).addListener(i,"dblclick",L.DomEvent.stopPropagation).addListener(i,"click",function(){var t=this.link;L.DomUtil.hasClass(t,"leaflet-credits-showlink")?L.DomUtil.removeClass(t,"leaflet-credits-showlink"):L.DomUtil.addClass(t,"leaflet-credits-showlink")}),this._container=i,this._link=o,i},setText:function(t){this._link.innerHTML=t}});
// a simple control to display a logo and credits in the corner of the map, with some neat interactive behavior
// in Leaflet tradition, a shortcut method is also provided, so you may use either version:
//     new L.CreditsControl(options)
//     L.controlCredits(options)
L.controlCredits = function (options) {
    return new L.CreditsControl(options);
}

L.CreditsControl = L.Control.extend({
    options: {
        position: 'bottomright'
    },
    initialize: function(options) {
        if (! options.text)  throw "L.CreditsControl missing required option: text";
        if (! options.image) throw "L.CreditsControl missing required option: image";
        if (! options.link)  throw "L.CreditsControl missing required option: link";

        L.setOptions(this,options);
    },
    onAdd: function (map) {
        this._map = map;

        // create our container, and set the background image
        var container = L.DomUtil.create('div', 'leaflet-credits-control', container);
        container.style.backgroundImage = 'url(' + this.options.image + ')';
        if (this.options.width)  container.style.paddingRight = this.options.width + 'px';
        if (this.options.height) container.style.height       = this.options.height + 'px';

        // generate the hyperlink to the left-hand side
        var link        = L.DomUtil.create('a', '', container);
        link.target     = '_blank';
        link.href       = this.options.link;
        link.innerHTML  = this.options.text;

        // create a linkage between this control and the hyperlink bit, since we will be toggling CSS for that hyperlink section
        container.link = link;

        // clicking the control (the image bit) expands the left-hand hyperlink/text bit
        L.DomEvent
        .addListener(container, 'mousedown', L.DomEvent.stopPropagation)
        .addListener(container, 'click', L.DomEvent.stopPropagation)
        .addListener(container, 'dblclick', L.DomEvent.stopPropagation)
        .addListener(container, 'click', function () {
            var link = this.link;
            if ( L.DomUtil.hasClass(link, 'leaflet-credits-showlink') ) {
                L.DomUtil.removeClass(link, 'leaflet-credits-showlink');
            } else {
                L.DomUtil.addClass(link, 'leaflet-credits-showlink');
            }
        });

        // afterthought keep a reference to our container and to the link,
        // in case we need to change their content later via setText() et al
        this._container = container;
        this._link      = link;

        // all done
        return container;
    },
    setText: function (html) {
        this._link.innerHTML = html;
    }
});