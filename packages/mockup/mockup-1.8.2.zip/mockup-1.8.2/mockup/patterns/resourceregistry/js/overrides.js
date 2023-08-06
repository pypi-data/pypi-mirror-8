/* global alert:true, confirm:true */

define([
  'jquery',
  'underscore',
  'mockup-ui-url/views/base',
  'mockup-patterns-texteditor',
  'mockup-utils'
], function($, _, BaseView, TextEditor, utils) {
  'use strict';

  var OverrideResource = BaseView.extend({
    tagName: 'li',
    className: 'list-group-item',
    template: _.template('<a href="#"><%- filepath %></a> ' +
      '<div class="plone-btn-group pull-right">' +
        '<button class="plone-btn plone-btn-danger plone-btn-xs">Delete</button>' +
        '<% if(view.canSave) { %> ' +
          '<button class="plone-btn plone-btn-primary plone-btn-xs">Save</button> ' +
          '<button class="plone-btn plone-btn-default plone-btn-xs">Cancel</button> ' +
        ' <% } %>' +
      '</div>'),

    events: {
      'click a': 'itemClicked',
      'click button.plone-btn-danger': 'itemDeleted',
      'click button.plone-btn-primary': 'itemSaved',
      'click button.plone-btn-default': 'itemCancel'
    },
    canSave: false,

    initialize: function(options){
      BaseView.prototype.initialize.apply(this, [options]);
      this.tabView = this.options.overridesView.tabView;
      this.loading = this.tabView.loading;
    },

    serializedModel: function(){
      return $.extend({}, { view: this }, this.options);
    },

    itemSaved: function(e){
      e.preventDefault();
      var self = this;
      self.tabView.saveData('save-file', {
        filepath: self.options.filepath,
        data: self.editor.editor.getValue()
      }, function(){
        self.canSave = false;
        self.render();
      });
    },

    itemDeleted: function(e){
      e.preventDefault();
      var self = this;
      if(confirm('Are you sure you want to delete this override?')){
        this.options.data.overrides.splice(self.options.index, 1);
        this.render();
        self.tabView.saveData('delete-file', {
          filepath: self.options.filepath
        }, function(){
          var index = _.indexOf(self.options.overridesView.data.overrides, self.options.filepath);
          if(index !== -1){
            self.options.overridesView.data.overrides.splice(index, 1);
          }
          self.options.overridesView.render();
          self.loading.hide();
        });
      }
    },

    itemCancel: function(e){
      e.preventDefault();
      this.editor.$el.remove();
      this.canSave = false;
      this.render();
    },

    itemClicked: function(e){
      var self = this;
      e.preventDefault();
      var data = self.options.data;
      var override = data.overrides[self.options.index];
      var url = data.baseUrl;
      if(url[url.length - 1] !== '/'){
        url += '/';
      }
      self.loading.show();
      $.ajax({
        // cache busting url
        url: url + override + '?' + utils.generateId(),
        dataType: 'text'
      }).done(function(data){
        var $pre = $('<pre class="pat-texteditor" />');
        $pre.html(data);
        self.options.overridesView.$editorContainer.empty().append($pre);
        self.editor = new TextEditor($pre, {
          width: 600,
          height: 500
        });
        self.editor.setSyntax(override);
        self.editor.editor.on('change', function(){
          if(!self.canSave){
            self.canSave = true;
            self.render();
          }
        });
        self.render();
        self.loading.hide();
      }).fail(function(){
        alert('error loading resource for editing');
        self.loading.hide();
      });
    }
  });


  var OverridesView = BaseView.extend({
    tagName: 'div',
    className: 'tab-pane overrides',
    template: _.template(
      '<form class="row">' +
        '<div class="col-md-6 col-md-offset-6">' +
          '<div class="input-group">' +
            '<input type="text" class="form-control search-field" />' +
            '<span class="input-group-btn">' +
              '<button class="plone-btn plone-btn-default" type="button">Search</button>' +
            '</span>' +
          '</div>' +
        '</div>' +
      '</form>' +
      '<div class="row">' +
        '<ul class="items list-group col-md-5"></ul>' +
        '<div class="col-md-7">' +
          '<ul class="hidden list-group search-results" />' +
          '<div class="editor" />' +
        '</div>' +
      '</div>'),
    events: {
      'submit form': 'noSubmit',
      'keyup form input': 'textChange',
      'click button.clear': 'clearSearchResults',
      'click button.customize': 'customizeResource'
    },

    noSubmit: function(e){
      e.preventDefault();
    },

    clearSearchResults: function(e){
      e.preventDefault();
      this.$searchResults.addClass('hidden');
      this.$searchInput.attr('value', '');
    },

    customizeResource: function(e){
      e.preventDefault();
      var $btn = $(e.target);
      this.options.data.overrides.push($btn.parent().find('span').html());
      this.render();
    },

    textChange: function(){
      var self = this;
      var q = self.$searchInput.val();
      if(q.length < 4){
        self.$searchResults.addClass('hidden');
        return;
      }
      q = q.toLowerCase();
      self.$searchResults.empty().removeClass('hidden');
      self.$searchResults.append('<li class="list-group-item list-group-item-warning">' +
        'Results<button class="plone-btn plone-btn-default pull-right plone-btn-xs clear">Clear</button></li>');
      var matches = [];
      var data = self.options.data;
      var urlMatches = function(base, path){
        var filepath = (base + (path || '')).toLowerCase();
        if(filepath.indexOf('++plone++') === -1){
          return false;
        }
        return filepath.indexOf(q) !== -1;
      };
      _.each(data.resources, function(resource){
        var base = resource.url || '';
        if(base){
          base += '/';
        }
        if(urlMatches(base, resource.js)){
          matches.push(base + resource.js);
        }
        for(var i=0; i<resource.css.length; i=i+1){
          if(urlMatches(base, resource.css[i])){
            matches.push(base + resource.css[i]);
          }
        }
      });
      _.each(matches, function(filepath){
        self.$searchResults.append(
          '<li class="list-group-item"><span>' + filepath + '</span> ' +
          '<button class="plone-btn plone-btn-danger pull-right plone-btn-xs customize">Customize</button></li>'
        );
      });
    },

    afterRender: function(){
      var self = this;
      self.$ul = self.$('ul.items');
      _.each(self.options.data.overrides, function(filepath, index){
        var view = new OverrideResource({
          index: index,
          filepath: filepath,
          overridesView: self,
          data: self.options.data
        });
        self.$ul.append(view.render().el);
      });
      self.$editorContainer = self.$('.editor');
      self.$searchInput = self.$('form input');
      self.$searchResults = self.$('.search-results');
    }
  });

  return OverridesView;
});
