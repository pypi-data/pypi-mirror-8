this["ds"] = this["ds"] || {};
this["ds"]["templates"] = this["ds"]["templates"] || {};

this["ds"] = this["ds"] || {};
this["ds"]["templates"] = this["ds"]["templates"] || {};
this["ds"]["templates"]["edit"] = this["ds"]["templates"]["edit"] || {};

this["ds"] = this["ds"] || {};
this["ds"]["templates"] = this["ds"]["templates"] || {};
this["ds"]["templates"]["flot"] = this["ds"]["templates"]["flot"] || {};

this["ds"] = this["ds"] || {};
this["ds"]["templates"] = this["ds"]["templates"] || {};
this["ds"]["templates"]["listing"] = this["ds"]["templates"]["listing"] || {};

this["ds"] = this["ds"] || {};
this["ds"]["templates"] = this["ds"]["templates"] || {};
this["ds"]["templates"]["models"] = this["ds"]["templates"]["models"] || {};

Handlebars.registerPartial("action-menu-button", this["ds"]["templates"]["action-menu-button"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n  <li role=\"presentation\"\n    data-ds-action=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n    data-ds-category=\"";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n    data-ds-show=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.show)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-ds-hide=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.hide)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    <a role=\"menuitem\" href=\"#\"><i class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.icon)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i> "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.display)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</a>\n";
  return buffer;
  }

  stack1 = helpers.each.call(depth0, (depth0 && depth0.actions), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-action-menu", this["ds"]["templates"]["ds-action-menu"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<div data-ds-hide=\"edit\" class=\"btn-group\" align=\"left\">\n  <button type=\"button\"\n          class=\"btn btn-default btn-xs dropdown-toggle\"\n          data-toggle=\"dropdown\">\n    <span class=\"caret\"></span>\n  </button>\n  <ul class=\"dropdown-menu dropdown-menu-right ds-action-menu\" role=\"menu\">\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "presentation-transform-actions", options) : helperMissing.call(depth0, "actions", "presentation-transform-actions", options)))
    + "\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "presentation-actions", true, options) : helperMissing.call(depth0, "actions", "presentation-actions", true, options)))
    + "\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_type), true, options) : helperMissing.call(depth0, "actions", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_type), true, options)))
    + "\n  </ul>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-dashboard-listing-action-menu", this["ds"]["templates"]["ds-dashboard-listing-action-menu"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"btn-group\">\n  <button\n     type=\"button\"\n     class=\"btn btn-default btn-xs dropdown-toggle\"\n     data-toggle=\"dropdown\">\n    <span class=\"caret\"></span>\n  </button>\n  <ul class=\"dropdown-menu dropdown-menu-right ds-dashboard-action-menu\" role=\"menu\" data-ds-href=\"";
  if (helper = helpers.href) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.href); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" data-ds-view-href=\"";
  if (helper = helpers.view_href) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.view_href); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "dashboard-list-actions", options) : helperMissing.call(depth0, "actions", "dashboard-list-actions", options)))
    + "\n  </ul>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-dashboard-listing-entry", this["ds"]["templates"]["ds-dashboard-listing-entry"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n            <br/>\n            <small>";
  if (helper = helpers.summary) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.summary); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</small>\n            ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n          ";
  stack1 = self.invokePartial(partials['ds-dashboard-tag-with-link'], 'ds-dashboard-tag-with-link', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n          ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n          <a href=\"";
  if (helper = helpers.imported_from) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.imported_from); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" target=\"_blank\"><i class=\"fa fa-cloud\"></i></a><br/>\n          ";
  return buffer;
  }

  buffer += "<tr data-ds-href=\"";
  if (helper = helpers.href) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.href); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n  <td>\n    <div class=\"row\">\n      <div class=\"\"> <!-- col-md-1 -->\n        <!-- <a href=\"/dashboards/";
  if (helper = helpers.id) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.id); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"><i class=\"fa fa-2x fa-dashboard\"></i></a> -->\n      </div>\n      <div class=\"col-md-12\">\n\n        <div class=\"pull-left\">\n          <a href=\"";
  if (helper = helpers.view_href) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.view_href); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n            <span class=\"ds-dashboard-listing-category\">\n              ";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\n            </span>\n            <span class=\"ds-dashboard-listing-title\">\n              ";
  if (helper = helpers.title) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.title); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\n            </span>\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.summary), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n          </a><br/>\n          <span class=\"ds-dashboard-listing-last-modified\">\n            Last modified "
    + escapeExpression((helper = helpers.moment || (depth0 && depth0.moment),options={hash:{},data:data},helper ? helper.call(depth0, "fromNow", (depth0 && depth0.last_modified_date), options) : helperMissing.call(depth0, "moment", "fromNow", (depth0 && depth0.last_modified_date), options)))
    + ".\n          </span>\n        </div>\n\n        <div class=\"pull-right\" style=\"margin-left: 0.5em\">\n          ";
  stack1 = self.invokePartial(partials['ds-dashboard-listing-action-menu'], 'ds-dashboard-listing-action-menu', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </div>\n\n        <div class=\"pull-right\" style=\"text-align:right\">\n          ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.tags), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n          <br/>\n          ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.imported_from), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </div>\n\n      </div>\n\n    </div> <!-- row -->\n  </td>\n</tr>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-dashboard-tag-with-link", this["ds"]["templates"]["ds-dashboard-tag-with-link"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, functionType="function", escapeExpression=this.escapeExpression, self=this;


  buffer += "<a href=\"/dashboards/tagged/";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">";
  stack1 = self.invokePartial(partials['ds-dashboard-tag'], 'ds-dashboard-tag', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</a>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-dashboard-tag", this["ds"]["templates"]["ds-dashboard-tag"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n    background-color: ";
  if (helper = helpers.bgcolor) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.bgcolor); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + ";\n  ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n    color: ";
  if (helper = helpers.fgcolor) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.fgcolor); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + ";\n  ";
  return buffer;
  }

  buffer += "<span class=\"badge badge-neutral\" data-ds-tag=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n  style=\"\n  ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.bgcolor), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.fgcolor), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += ">\n  \">\n  ";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\n</span>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar-cell", this["ds"]["templates"]["ds-edit-bar-cell"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"ds-edit-bar ds-edit-bar-cell alert alert-info\" align=\"left\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  <span class=\"badge ds-badge-cell\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"><i class=\"fa fa-cog\"></i> cell "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n  <div class=\"btn-group btn-group-sm\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" style=\"display:none\">\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "edit-bar-cell", "button", options) : helperMissing.call(depth0, "actions", "edit-bar-cell", "button", options)))
    + "\n  </div>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar-item-details", this["ds"]["templates"]["ds-edit-bar-item-details"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;


  buffer += "<div class=\"row\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "-details\">\n  <div class=\"col-md-12\">\n    ";
  stack1 = self.invokePartial(partials['ds-item-property-sheet'], 'ds-item-property-sheet', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar-item", this["ds"]["templates"]["ds-edit-bar-item"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"row\" data-ds-show=\"edit\" style=\"display:none\">\n  <div class=\"col-md-12\">\n    <div class=\"ds-edit-bar ds-edit-bar-item\" align=\"left\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n      <span class=\"badge ds-badge-item\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"><i class=\"fa fa-cog\"></i> "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_type)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n      <div class=\"btn-group btn-group-sm\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" style=\"display:none\">\n        "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "edit-bar-item", "button", options) : helperMissing.call(depth0, "actions", "edit-bar-item", "button", options)))
    + "\n      </div>\n    </div>\n  </div>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar-row", this["ds"]["templates"]["ds-edit-bar-row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "    <div class=\"ds-edit-bar ds-edit-bar-row\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n      <span class=\"badge ds-badge-row\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"><i class=\"fa fa-cog\"></i> row "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n      <div class=\"btn-group btn-group-sm\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" style=\"display:none\">\n        "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "edit-bar-row", "button", options) : helperMissing.call(depth0, "actions", "edit-bar-row", "button", options)))
    + "\n      </div>\n    </div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar-section", this["ds"]["templates"]["ds-edit-bar-section"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "    <div class=\"ds-edit-bar ds-edit-bar-section\" align=\"left\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n      <span class=\"badge ds-badge-section\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"><i class=\"fa fa-cog\"></i> section "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n      <div class=\"btn-group btn-group-sm\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" style=\"display:none\">\n        "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "edit-bar-section", "button", options) : helperMissing.call(depth0, "actions", "edit-bar-section", "button", options)))
    + "\n      </div>\n    </div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-bar", this["ds"]["templates"]["ds-edit-bar"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"row\" data-ds-show=\"edit\" style=\"display:none\">\n  <div class=\"col-md-12\">\n    <i title=\"Drag to reposition\" class=\"fa fa-align-justify pull-right ds-drag-handle\" data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i>\n    "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  </div>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-edit-menu", this["ds"]["templates"]["ds-edit-menu"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<div data-ds-show=\"edit\" class=\"btn-group\" align=\"left\" style=\"display:none\">\n  <button type=\"button\"\n          class=\"btn btn-default btn-xs dropdown-toggle\"\n          data-toggle=\"dropdown\">\n          <i class=\"fa fa-cog\"></i> <span class=\"caret\"></span>\n  </button>\n  <ul class=\"dropdown-menu dropdown-menu-right ds-edit-menu\" role=\"menu\">\n    "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "presentation-edit", options) : helperMissing.call(depth0, "actions", "presentation-edit", options)))
    + "\n  </ul>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-row-edit-bar", this["ds"]["templates"]["ds-row-edit-bar"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"row\" data-ds-show=\"edit\">\n  <div class=\"col-md-12\">\n    <div class=\"ds-edit-bar ds-row-edit-bar bs-callout bs-callout-info\">\n\n\n\n\n      row <i class=\"fa fa-trash-o pull-right\"></i>\n\n\n\n    </div>\n  </div>\n</div>\n";
  }));

Handlebars.registerPartial("ds-title-bar", this["ds"]["templates"]["ds-title-bar"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "<h3>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h3>";
  return buffer;
  }

  buffer += escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n<div class=\"row\">\n  <div class=\"col-md-10\">\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n  <div class=\"col-md-2\" align=\"right\">\n    ";
  stack1 = self.invokePartial(partials['ds-action-menu'], 'ds-action-menu', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("dashboard-metadata-panel", this["ds"]["templates"]["edit"]["dashboard-metadata-panel"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, self=this, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n            ";
  stack1 = self.invokePartial(partials['ds-dashboard-tag'], 'ds-dashboard-tag', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n          <tr>\n            <th>Imported From</th><td class=\"ds-editable\" id=ds-info-panel-edit-imported-from\" data-type=\"text\"><a href=\"";
  if (helper = helpers.imported_from) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.imported_from); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" target=\"_blank\">Link</a></td>\n          </tr>\n        ";
  return buffer;
  }

  buffer += "<div class=\"row ds-info-edit-panel\">\n  <!-- Column 1 -->\n  <div class=\"col-md-5\">\n    <h4>Properties</h4>\n\n    <table class=\"table-condensed\">\n      <tbody>\n        <tr>\n          <th>Title</th><td class=\"ds-editable\" id=\"ds-info-panel-edit-title\" data-type=\"text\">";
  if (helper = helpers.title) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.title); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</td>\n        </tr>\n\n        <tr>\n          <th>Category</th><td class=\"ds-editable\" id=\"ds-info-panel-edit-category\" data-type=\"text\">";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</td>\n        </tr>\n\n        <tr>\n          <th>Summary</th><td class=\"ds-editable\" id=\"ds-info-panel-edit-summary\" data-type=\"text\">";
  if (helper = helpers.summary) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.summary); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</td>\n        </tr>\n\n        <tr>\n          <th>Tags</th>\n          <td>\n            <!--\n            ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.tags), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            -->\n\n            <input id=\"ds-info-panel-edit-tags\" class=\"form-control tm-input tm-input-success tm-input-info\"/>\n\n          </td>\n        </tr>\n\n        <tr>\n          <th>Created</th><td>"
    + escapeExpression((helper = helpers.moment || (depth0 && depth0.moment),options={hash:{},data:data},helper ? helper.call(depth0, "MMMM Do YYYY, h:mm:ss a", (depth0 && depth0.creation_date), options) : helperMissing.call(depth0, "moment", "MMMM Do YYYY, h:mm:ss a", (depth0 && depth0.creation_date), options)))
    + "</td>\n        </tr>\n        <tr>\n          <th>Last Modified</th><td>"
    + escapeExpression((helper = helpers.moment || (depth0 && depth0.moment),options={hash:{},data:data},helper ? helper.call(depth0, "MMMM Do YYYY, h:mm:ss a", (depth0 && depth0.last_modified_date), options) : helperMissing.call(depth0, "moment", "MMMM Do YYYY, h:mm:ss a", (depth0 && depth0.last_modified_date), options)))
    + "</td>\n        </tr>\n\n        ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.imported_from), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n      </tbody>\n    </table>\n  </div> <!-- column -->\n\n  <!-- Column 2 -->\n  <div class=\"col-md-7\">\n    <h4>Description</h4>\n    <div class=\"ds-editable\"\n         id=\"ds-info-panel-edit-description\"\n         data-type=\"textarea\"\n         data-rows=\"9\"\n         data-showbuttons=\"bottom\"\n         data-inputclass=\"ds-dashboard-description\"\n         style=\"text-align:top;\">\n      "
    + escapeExpression((helper = helpers.markdown || (depth0 && depth0.markdown),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.description), options) : helperMissing.call(depth0, "markdown", (depth0 && depth0.description), options)))
    + "\n    </div>\n  </div>\n\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("dashboard-query-panel", this["ds"]["templates"]["edit"]["dashboard-query-panel"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, self=this, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n          ";
  stack1 = self.invokePartial(partials['dashboard-query-row'], 'dashboard-query-row', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        ";
  return buffer;
  }

  buffer += "<div class=\"ds-query-edit-panel\" id=\"ds-query-panel\">\n\n  <div class=\"row\">\n    <div class=\"col-md-12\">\n      <div class=\"btn-group btn-group-sm\">\n        "
    + escapeExpression((helper = helpers.actions || (depth0 && depth0.actions),options={hash:{},data:data},helper ? helper.call(depth0, "dashboard-queries", "button", options) : helperMissing.call(depth0, "actions", "dashboard-queries", "button", options)))
    + "\n      </div>\n      <br/>\n    </div>\n  </div>\n\n  <div class=\"row\">\n    <div class=\"col-md-12\">\n      <table class=\"table table-striped\">\n        ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.definition)),stack1 == null || stack1 === false ? stack1 : stack1.queries), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </table>\n    </div>\n  </div>\n\n</div>\n";
  return buffer;
  }));

Handlebars.registerPartial("dashboard-query-row", this["ds"]["templates"]["edit"]["dashboard-query-row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<tr data-ds-query-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n  <th data-ds-query-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" class=\"ds-query-name\">";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</th>\n  <td data-ds-query-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" class=\"ds-query-target\">";
  if (helper = helpers.targets) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.targets); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</td>\n  <td>\n    <div class=\"btn-group\">\n      <button class=\"btn btn-default btn-small ds-duplicate-query-button\"\n              data-toggle=\"tooltip\"\n              title=\"Duplicate this query\"\n              data-ds-query-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n        <i class=\"fa fa-copy\"></i>\n      </button>\n      <button class=\"btn btn-default btn-small ds-delete-query-button\"\n              data-toggle=\"tooltip\"\n              title=\"Delete this query\"\n              data-ds-query-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n        <i class=\"fa fa-trash-o\"></i>\n      </button>\n    </div>\n  </td>\n</tr>\n";
  return buffer;
  }));

Handlebars.registerPartial("ds-item-property-sheet", this["ds"]["templates"]["edit"]["ds-item-property-sheet"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data,depth1) {
  
  var buffer = "", stack1, helper, options;
  buffer += "\n      <tr>\n        <td><span class=\"ds-property-category\">";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.category), {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "<span class=\"ds-property-name\">";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</span></td>\n        <td data-ds-property-name=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">"
    + escapeExpression((helper = helpers.interactive_property || (depth0 && depth0.interactive_property),options={hash:{},data:data},helper ? helper.call(depth0, depth0, (depth1 && depth1.item), options) : helperMissing.call(depth0, "interactive_property", depth0, (depth1 && depth1.item), options)))
    + "</td>\n      </tr>\n    ";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "", stack1, helper;
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</span> / ";
  return buffer;
  }

  buffer += "<table class=\"ds-property-sheet\">\n  <tbody>\n    <tr><th>Property</th><th>Value</th></tr>\n    ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.interactive_properties), {hash:{},inverse:self.noop,fn:self.programWithDepth(1, program1, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </tbody>\n</table>\n";
  return buffer;
  }));

this["ds"]["templates"]["action-menu-button"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.divider), {hash:{},inverse:self.program(4, program4, data),fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n        <li class=\"divider\" data-ds-show=\"";
  if (helper = helpers.show) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.show); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\" data-ds-hide=\"";
  if (helper = helpers.hide) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.hide); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"/>\n      ";
  return buffer;
  }

function program4(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n        <li class=\"";
  if (helper = helpers['class']) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0['class']); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n          role=\"presentation\"\n          data-ds-action=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n          data-ds-category=\"";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n          data-ds-show=\"";
  if (helper = helpers.show) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.show); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n          data-ds-hide=\"";
  if (helper = helpers.hide) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.hide); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n          <a role=\"menuitem\" href=\"#\"><i class=\"fa-fw ";
  if (helper = helpers.icon) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.icon); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"></i> ";
  if (helper = helpers.display) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.display); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</a>\n        </li>\n      ";
  return buffer;
  }

  buffer += "<div class=\"btn-group btn-group-sm\" align=\"left\">\n  <button type=\"button\"\n    class=\"btn btn-default dropdown-toggle "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1['class'])),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-toggle=\"dropdown\"\n    title=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.display)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    <i class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.icon)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i> <span class=\"caret\"></span>\n  </button>\n  <ul class=\"dropdown-menu dropdown-menu-left ds-edit-menu\" role=\"menu\">\n    ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.actions), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </ul>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["action"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n  <li class=\"divider\" data-ds-show=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.show)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" data-ds-hide=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.hide)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"/>\n";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n  <li role=\"presentation\"\n    data-ds-action=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-ds-category=\"";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n    data-ds-show=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.show)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-ds-hide=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.hide)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    <a role=\"menuitem\" href=\"#\"><i class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.icon)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i> "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.display)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</a>\n  </li>\n";
  return buffer;
  }

  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.divider), {hash:{},inverse:self.program(3, program3, data),fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });

this["ds"]["templates"]["action_button"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "\n";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n  <button class=\"btn ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1['class']), {hash:{},inverse:self.program(6, program6, data),fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n    data-ds-action=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-ds-category=\"";
  if (helper = helpers.category) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.category); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"\n    data-ds-show=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.show)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-ds-hide=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.hide)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n    data-toggle=\"tooltip\"\n    title=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.display)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    <i class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.icon)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i>\n  </button>\n";
  return buffer;
  }
function program4(depth0,data) {
  
  var stack1;
  return escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1['class'])),typeof stack1 === functionType ? stack1.apply(depth0) : stack1));
  }

function program6(depth0,data) {
  
  
  return "btn-default";
  }

  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.action)),stack1 == null || stack1 === false ? stack1 : stack1.divider), {hash:{},inverse:self.program(3, program3, data),fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });

this["ds"]["templates"]["edit"]["dashboard_panel"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, self=this;


  buffer += "<ul class=\"nav nav-pills\">\n  <li class=\"active\"><a href=\"#metadata\" data-toggle=\"tab\">Metadata</a></li>\n  <li><a href=\"#queries\" data-toggle=\"tab\">Queries</a></li>\n</ul>\n\n<div class=\"tab-content\">\n  <div class=\"tab-pane active\" id=\"metadata\">\n    ";
  stack1 = self.invokePartial(partials['dashboard-metadata-panel'], 'dashboard-metadata-panel', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n  <div class=\"tab-pane\" id=\"queries\">\n    ";
  stack1 = self.invokePartial(partials['dashboard-query-panel'], 'dashboard-query-panel', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </div>\n\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["edit"]["item_source"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


  buffer += "<div class=\"ds-item-source\">\n  <pre>"
    + escapeExpression((helper = helpers.json || (depth0 && depth0.json),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "json", (depth0 && depth0.item), options)))
    + "</pre>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["flot"]["tooltip"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, helper, options;
  buffer += "\n      <tr>\n        <td class=\"ds-tooltip-label\">\n          <span class=\"badge\" style=\"background-color: "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.color)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"><i></i></span>\n          "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.label)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n        </td>\n        <td class=\"ds-tooltip-value\">\n          "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ",.3s", (depth0 && depth0.value), options) : helperMissing.call(depth0, "format", ",.3s", (depth0 && depth0.value), options)))
    + "\n        </td>\n      </tr>\n    ";
  return buffer;
  }

  buffer += "<table class=\"table-condensed\">\n  <tbody>\n    <tr>\n      <td>\n        <span class=\"ds-tooltip-time\">"
    + escapeExpression((helper = helpers.moment || (depth0 && depth0.moment),options={hash:{},data:data},helper ? helper.call(depth0, "dd, M-D-YYYY, h:mm A", (depth0 && depth0.time), options) : helperMissing.call(depth0, "moment", "dd, M-D-YYYY, h:mm A", (depth0 && depth0.time), options)))
    + "</span>\n      </td>\n    </tr>\n    ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </tbody>\n</table>\n";
  return buffer;
  });

this["ds"]["templates"]["listing"]["dashboard_list"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      ";
  stack1 = self.invokePartial(partials['ds-dashboard-listing-entry'], 'ds-dashboard-listing-entry', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  return buffer;
  }

function program3(depth0,data) {
  
  
  return "\n      <tr><td><h3>No dashboards defined</h3></td></tr>\n    ";
  }

  buffer += "<table class=\"table table-hover table-condensed\">\n  <tbody>\n    ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.dashboards), {hash:{},inverse:self.program(3, program3, data),fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  </tbody>\n</table>\n";
  return buffer;
  });

this["ds"]["templates"]["listing"]["dashboard_tag_list"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "active";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n  <li data-ds-tag=\"";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n    <a href=\"/dashboards/tagged/";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\">\n      ";
  if (helper = helpers.name) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.name); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\n      <span class=\"badge badge-primary pull-right\">";
  if (helper = helpers.count) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.count); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</span>\n    </a>\n  </li>\n  ";
  return buffer;
  }

  buffer += "<ul class=\"nav nav-pills nav-stacked\">\n  <li class=\"";
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.tag), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <a href=\"/dashboards\">\n      All <span class=\"badge badge-primary pull-right\"></span>\n    </a>\n  </li>\n\n    ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.tags), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</ul>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["cell"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += " align=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.align)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "<div class=\""
    + escapeExpression((helper = helpers.style_class || (depth0 && depth0.style_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "style_class", (depth0 && depth0.item), options)))
    + "\">";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "\n    "
    + escapeExpression((helper = helpers.item || (depth0 && depth0.item),options={hash:{},data:data},helper ? helper.call(depth0, depth0, options) : helperMissing.call(depth0, "item", depth0, options)))
    + "\n    ";
  return buffer;
  }

function program7(depth0,data) {
  
  
  return "</div>";
  }

  buffer += "<div class=\"ds-cell "
    + escapeExpression((helper = helpers.span || (depth0 && depth0.span),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "span", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.offset || (depth0 && depth0.offset),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "offset", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"\n     ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.align), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += " id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"\n       >\n       ";
  stack1 = self.invokePartial(partials['ds-edit-bar'], 'ds-edit-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n    ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.items), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      <i data-ds-show=\"\"\n        style=\"display:none\"\n        title=\"Drag to resize\"\n        class=\"fa fa-arrows-alt pull-right ds-resize-handle\"\n        data-ds-item-id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></i>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["comparison_summation_table"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  
  return "table-striped";
  }

function program3(depth0,data) {
  
  var stack1;
  return escapeExpression(((stack1 = ((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.query_other)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1));
  }

function program5(depth0,data) {
  
  var stack1;
  return escapeExpression(((stack1 = ((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.query)),stack1 == null || stack1 === false ? stack1 : stack1.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1));
  }

  buffer += "<div class=\"ds-item\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <table class=\"table table-condensed ds-timeshift-summation-table "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\n                ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.striped), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <thead>\n      <tr>\n        <th></th>\n        <th>";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.query_other), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</th>\n        <th>";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.query), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</th>\n        <th>Delta</th>\n        <th>%</th>\n      </tr>\n    </thead>\n    <tbody/>\n  </table>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["comparison_summation_table_body"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function";


  buffer += "<!-- TODO: configure which rows to include. Sum doesnt make sense for rates -->\n<tr>\n  <th>Average</th>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Min</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Max</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Sum</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["definition"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;

function program1(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "\n    "
    + escapeExpression((helper = helpers.item || (depth0 && depth0.item),options={hash:{},data:data},helper ? helper.call(depth0, depth0, options) : helperMissing.call(depth0, "item", depth0, options)))
    + "\n  ";
  return buffer;
  }

  buffer += "<div class=\""
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + " ds-dashboard\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["donut_chart"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;


  buffer += "<div class=\"ds-item ds-graph ds-donut-chart "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\"\n  id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"ds-graph-holder "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <svg class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"></svg>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["heading"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.css_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "<small>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.description)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</small>";
  return buffer;
  }

  buffer += "<div class=\"ds-item ds-heading\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  <h"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.level)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.css_class), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += ">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.text)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.description), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </h"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.level)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + ">\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["jumbotron_singlestat"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"ds-item ds-jumbotron-singlestat\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  <div class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\"\n    >\n    <div><p><span class=\"value\"></span><span class=\"unit\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.units)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span></p></div>\n    <div><h3>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h3></div>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["markdown"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <pre>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.text)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</pre>\n  ";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n   ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.expanded_text), {hash:{},inverse:self.program(6, program6, data),fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  return buffer;
  }
function program4(depth0,data) {
  
  var stack1, helper, options;
  return escapeExpression((helper = helpers.markdown || (depth0 && depth0.markdown),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.expanded_text), options) : helperMissing.call(depth0, "markdown", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.expanded_text), options)));
  }

function program6(depth0,data) {
  
  var stack1, helper, options;
  return escapeExpression((helper = helpers.markdown || (depth0 && depth0.markdown),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.text), options) : helperMissing.call(depth0, "markdown", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.text), options)));
  }

  buffer += "<div class=\"ds-item ds-markdown "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.raw), {hash:{},inverse:self.program(3, program3, data),fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["percentage_table"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;


  buffer += "<div class=\"ds-item\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"ds-percentage-table-holder\">\n    <h4>No data</h4>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["percentage_table_data"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  
  return "\n        <th></th>\n        <th>Total</th>\n      ";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n        <th>";
  if (helper = helpers.target) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.target); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "</th>\n      ";
  return buffer;
  }

function program5(depth0,data) {
  
  
  return "\n        <th>%</th>\n        <th></th>\n      ";
  }

function program7(depth0,data) {
  
  var buffer = "", stack1, helper, options;
  buffer += "\n        <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ",.2%", ((stack1 = (depth0 && depth0.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent), options) : helperMissing.call(depth0, "format", ",.2%", ((stack1 = (depth0 && depth0.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent), options)))
    + "</td>\n      ";
  return buffer;
  }

function program9(depth0,data,depth1) {
  
  var buffer = "", stack1, helper, options;
  buffer += "\n      <tr>\n        <th>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.transform)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</th>\n        <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.query)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent_value), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.query)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent_value), options)))
    + "</td>\n        ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.query)),stack1 == null || stack1 === false ? stack1 : stack1.data), {hash:{},inverse:self.noop,fn:self.programWithDepth(10, program10, data, depth1),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      </tr>\n    ";
  return buffer;
  }
function program10(depth0,data,depth2) {
  
  var buffer = "", stack1, helper, options;
  buffer += "\n          <td>"
    + escapeExpression((helper = helpers.format || (depth2 && depth2.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth2 && depth2.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent_value), options) : helperMissing.call(depth0, "format", ((stack1 = (depth2 && depth2.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.summation)),stack1 == null || stack1 === false ? stack1 : stack1.percent_value), options)))
    + "</td>\n        ";
  return buffer;
  }

  buffer += "<table class=\"table table-condensed ds-percentage-table\">\n\n  <thead>\n    <tr>\n      ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.include_sums), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.query)),stack1 == null || stack1 === false ? stack1 : stack1.data), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </tr>\n  </thead>\n\n  <tbody>\n    <tr>\n      ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.include_sums), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.query)),stack1 == null || stack1 === false ? stack1 : stack1.data), {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </tr>\n\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.include_sums), {hash:{},inverse:self.noop,fn:self.programWithDepth(9, program9, data, depth0),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n  </tbody>\n\n</table>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;

function program1(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "<div class=\""
    + escapeExpression((helper = helpers.style_class || (depth0 && depth0.style_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "style_class", (depth0 && depth0.item), options)))
    + "\">";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "\n        "
    + escapeExpression((helper = helpers.item || (depth0 && depth0.item),options={hash:{},data:data},helper ? helper.call(depth0, depth0, options) : helperMissing.call(depth0, "item", depth0, options)))
    + "\n      ";
  return buffer;
  }

function program5(depth0,data) {
  
  
  return "</div>";
  }

  buffer += "<div class=\"ds-row\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n    ";
  stack1 = self.invokePartial(partials['ds-edit-bar'], 'ds-edit-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    <div class=\"row "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\">\n      ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.items), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </div>\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["section"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;

function program1(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "<div class=\""
    + escapeExpression((helper = helpers.style_class || (depth0 && depth0.style_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "style_class", (depth0 && depth0.item), options)))
    + "\">";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n      <div>\n        <h1 class=\"ds-section-heading\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h1>\n        <hr/>\n      </div>\n    ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", helper, options;
  buffer += "\n      "
    + escapeExpression((helper = helpers.item || (depth0 && depth0.item),options={hash:{},data:data},helper ? helper.call(depth0, depth0, options) : helperMissing.call(depth0, "item", depth0, options)))
    + "\n    ";
  return buffer;
  }

function program7(depth0,data) {
  
  
  return "</div>";
  }

  buffer += "<div class=\"ds-section "
    + escapeExpression((helper = helpers.container_class || (depth0 && depth0.container_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "container_class", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-edit-bar'], 'ds-edit-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n    ";
  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.items), {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.style), {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["separator"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.css_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"";
  return buffer;
  }

  buffer += "<div class=\"ds-item ds-separator\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  <hr ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.css_class), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "></hr>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["simple_time_series"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;


  buffer += "<div class=\"ds-item ds-graph ds-simple-time-series "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"ds-graph-holder "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <svg class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"></svg>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["singlegraph"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;


  buffer += "<div class=\"ds-item ds-graph ds-singlegraph "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <span class=\"ds-label\"></span>\n  <span class=\"value\"></span>\n  <div class=\"ds-graph-holder "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <svg class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"></svg>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["singlestat"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


  buffer += "<div class=\"ds-item\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  "
    + escapeExpression((helper = helpers['ds-edit-bar'] || (depth0 && depth0['ds-edit-bar']),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "ds-edit-bar", (depth0 && depth0.item), options)))
    + "\n  <div class=\"ds-singlestat "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.css_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <h3>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.title)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h3>\n    <p><span class=\"value\"></span><span class=\"unit\">"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.units)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span></p>\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["stacked_area_chart"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;


  buffer += "<div class=\"ds-item ds-graph ds-stacked-area-chart "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\"\n  id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"ds-graph-holder "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <svg class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"></svg>\n  </div>\n  <div class=\"ds-legend-holder\" id=\"ds-legend-"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["standard_time_series"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function", self=this;


  buffer += "<div class=\"ds-item ds-graph ds-standard-time-series "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\"\n  id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <div class=\"ds-graph-holder "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\">\n    <svg class=\""
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + "\"></svg>\n  </div>\n  <div class=\"ds-legend-holder\" id=\"ds-legend-"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  </div>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["summation_table"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  
  return "table-striped";
  }

  buffer += "<div class=\"ds-item\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <table class=\"table table-condensed ds-summation-table "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\n                ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.striped), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <thead>\n      <tr>\n        <th></th>\n        <th>current</th>\n        <th>min</th>\n        <th>max</th>\n        <th>mean</th>\n        <th>median</th>\n        <th>sum</th>\n      </tr>\n    </thead>\n    <tbody>\n    </tbody>\n  </table>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["summation_table_row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1, helper;
  buffer += "\n      <span class=\"ds-summation-color-cell\" style=\"background:";
  if (helper = helpers.color) { stack1 = helper.call(depth0, {hash:{},data:data}); }
  else { helper = (depth0 && depth0.color); stack1 = typeof helper === functionType ? helper.call(depth0, {hash:{},data:data}) : helper; }
  buffer += escapeExpression(stack1)
    + "\"></span>\n    ";
  return buffer;
  }

  buffer += "<tr>\n    <th>\n    ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.show_color), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n      "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.target)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</th>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.last), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.last), options)))
    + "</td>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "</td>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "</td>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "</td>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.median), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.median), options)))
    + "</td>\n    <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = ((stack1 = (depth0 && depth0.series)),stack1 == null || stack1 === false ? stack1 : stack1.summation)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "</td>\n  </tr>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["timeshift_summation_table"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); partials = this.merge(partials, Handlebars.partials); data = data || {};
  var buffer = "", stack1, helper, options, functionType="function", escapeExpression=this.escapeExpression, self=this, helperMissing=helpers.helperMissing;

function program1(depth0,data) {
  
  
  return "table-striped";
  }

  buffer += "<div class=\"ds-item\" id=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.item_id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n  ";
  stack1 = self.invokePartial(partials['ds-title-bar'], 'ds-title-bar', depth0, helpers, partials, data);
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n  <table class=\"table table-condensed ds-timeshift-summation-table "
    + escapeExpression((helper = helpers.height || (depth0 && depth0.height),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "height", (depth0 && depth0.item), options)))
    + " "
    + escapeExpression((helper = helpers.css_class || (depth0 && depth0.css_class),options={hash:{},data:data},helper ? helper.call(depth0, (depth0 && depth0.item), options) : helperMissing.call(depth0, "css_class", (depth0 && depth0.item), options)))
    + "\n                ";
  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.striped), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <thead>\n      <tr>\n        <th></th>\n        <th>Now</th>\n        <th>"
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.shift)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + " Ago</th>\n        <th>Delta</th>\n        <th>%</th>\n      </tr>\n    </thead>\n    <tbody/>\n  </table>\n</div>\n";
  return buffer;
  });

this["ds"]["templates"]["models"]["timeshift_summation_table_body"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, functionType="function";


  buffer += "<!-- TODO: configure which rows to include. Sum doesnt make sense for rates -->\n<tr>\n  <th>Average</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.mean_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Median</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.median), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.median), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.median), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.median), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.median_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.median), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.median), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.median_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.median_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Min</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.min_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Max</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.max_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n<tr>\n  <th>Sum</th>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.now)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "</td>\n  <td>"
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.then)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "</td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression((helper = helpers.format || (depth0 && depth0.format),options={hash:{},data:data},helper ? helper.call(depth0, ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options) : helperMissing.call(depth0, "format", ((stack1 = (depth0 && depth0.item)),stack1 == null || stack1 === false ? stack1 : stack1.format), ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum), options)))
    + "\n  </td>\n  <td class=\""
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_class)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\n    "
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.diff)),stack1 == null || stack1 === false ? stack1 : stack1.sum_pct)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\n  </td>\n</tr>\n";
  return buffer;
  });