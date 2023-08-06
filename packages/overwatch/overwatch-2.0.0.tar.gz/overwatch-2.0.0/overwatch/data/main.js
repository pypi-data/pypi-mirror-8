$(window).ready(function() {
    //Handlebars.registerHelper('nl2br', function(text) {
        //var nl2br = (text + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + '<br>' + '$2');
        //return new Handlebars.SafeString(nl2br);
    //});

    var app = {};

    app.Model = Backbone.Model.extend({});
    app.Model.prototype.sync = function() { return null; };
    app.Model.prototype.fetch = function() { return null; };
    app.Model.prototype.save = function() { return null; };

    app.Collection = Backbone.Collection.extend({
        model: app.Model,
        initialize: function(){}
    });

    app.Project = app.Model.extend({});

    app.projectList = new (app.Collection.extend({url: '/', model: app.Project}));

    app.ProjectView = Backbone.View.extend({
        tagName: 'li',
        tpl: Handlebars.compile($('#project-tpl').html()),
        initialize: function() {
            this.model.on('destroy', this.remove, this);
        },
        render: function() {
            this.$el.html(this.tpl(this.model.attributes));
            return this;
        }
    });

    app.LogItem = app.Model.extend({});

    app.logItemList = new (app.Collection.extend({url: '/', model: app.LogItem}));

    app.LogItemView = Backbone.View.extend({
        tagName: 'li',
        className: 'hidden',
        attributes: {'tabindex': 0},
        colors: {
            'DEBUG': {bg: '#AAFFFF', text: '#007777'},
            'INFO': {bg: '#00AA00', text: '#FFFFFF'},
            'WARNING': {bg: '#AAAA00', text: '#FFFFFF'},
            'ERROR': {bg: '#AA0000', text: '#FFFFFF'},
            'EXCEPTION': {bg: '#AA0000', text: '#FFFFFF'}
        },
        tpl: Handlebars.compile($('#log-item-tpl').html()),
        render: function() {
            var levelname = this.model.get('data').levelname;
            this.$el.html(this.tpl({
                bg_color: this.colors[levelname].bg,
                text_color: this.colors[levelname].text,
                data: this.model.get('data'),
                project: this.model.get('project'),
            }));
            window.setTimeout(function() {
                this.$el.removeClass('hidden');
            }.bind(this), 20);
            return this;
        },
    });

    var host = window.location.protocol + '//' + window.location.host;
    console.log('Connecting to', host);
    var socket = io.connect(host);
    socket.on('connect', function() {
        console.log('Connected!');
        socket.emit('projects:get-list()')
//        socket.emit('my event', {data: 'I\'m connected!'});
    });
    socket.on('projects:new', function(data) {
        data = JSON.parse(data);
        var model = app.projectList.create(data);
        var projectView = new app.ProjectView({model: model});
        $('.projects').append(projectView.render().el);
    });
    socket.on('projects:remove', function(data) {
        data = JSON.parse(data);
        app.projectList.get(data.id).destroy();
    });
    socket.on('projects:list', function(data) {
        data = JSON.parse(data);
        for(key in data) {
            console.log(data[key]);
            var model = app.projectList.create(data[key]);
            var projectView = new app.ProjectView({model: model});
            $('.projects').append(projectView.render().el);
        }
    });
    socket.on('log-items:new', function(data) {
        data = JSON.parse(data);
        console.log(data);
        var model = app.logItemList.create(data);
        var logItemView = new app.LogItemView({model: model})
        $('.log-items').prepend(logItemView.render().el);
    });
    socket.on('ping', function(data) {
        console.log(data);
    });

    window.app = app;
});
