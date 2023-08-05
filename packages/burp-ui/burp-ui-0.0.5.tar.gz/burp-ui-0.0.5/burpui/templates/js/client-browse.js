
	/***
	 * Here is our tree to browse a specific backup
	 * The tree is first initialized with the 'root' part of the backup.
	 * JSON example:
	 * {
	 *   "results": [
	 *     {
	 *       "name": "/",
	 *       "parent": "",
	 *       "type": "d"
	 *     }
	 *   ]
	 * }
	 * This JSON is then parsed into another one to initialize our tree.
	 * Each 'directory' is expandable.
	 * A new JSON is returned for each one of then on-demand.
	 * JSON output:
	 * {
	 *   "results": [
	 *     {
	 *       "name": "etc", 
	 *       "parent": "/", 
	 *       "type": "d"
	 *     }, 
	 *     {
	 *       "name": "home", 
	 *       "parent": "/", 
	 *       "type": "d"
	 *     }
	 *   ]
	 * }
	 */
	$("#tree").fancytree({
		checkbox: true,
		selectMode: 3,
		extensions: ["glyph", "table", "gridnav", "filter"],
		glyph: {
			map: {
				doc: "glyphicon glyphicon-file",
				docOpen: "glyphicon glyphicon-file",
				checkbox: "glyphicon glyphicon-unchecked",
				checkboxSelected: "glyphicon glyphicon-check",
				checkboxUnknown: "glyphicon glyphicon-share",
				error: "glyphicon glyphicon-warning-sign",
				expanderClosed: "glyphicon glyphicon-plus-sign",
				expanderLazy: "glyphicon glyphicon-plus-sign",
				// expanderLazy: "glyphicon glyphicon-expand",
				expanderOpen: "glyphicon glyphicon-minus-sign",
				// expanderOpen: "glyphicon glyphicon-collapse-down",
				folder: "glyphicon glyphicon-folder-close",
				folderOpen: "glyphicon glyphicon-folder-open",
				loading: "icon-refresh-animate glyphicon glyphicon-refresh"
				// loading: "icon-spinner icon-spin"
			}
		},
		source: function() { 
			r = [];
			$.getJSON('{{ url_for("client_tree", name=cname, backup=nbackup, server=server) }}', function(data) {
				if (!data.results) {
					if (data.notif) {
						$.each(data.notif, function(i, n) {
							notif(n[0], n[1]);
						});
					}
					return;
				}
				$.each(data.results, function(j, c) {
					l = (c.type === "d");
					f = (c.type === "d");
					s = {title: c.name, key: c.name, lazy: l, folder: f, uid: c.uid, gid: c.gid, date: c.date, mode: c.mode, size: c.size, inodes: c.inodes};
					r.push(s);
				});
			});
			$("#waiting-container").hide();
			$("#tree-container").show();
			return r;
		},
		lazyLoad: function(event, data) {
			var node = data.node;
			// ugly hack to display a "loading" icon while retrieving data
			node._isLoading = true;
			node.renderStatus();
			r = [];
			p = node.key;
			if (p !== "/") p += '/';
			$.getJSON('{{ url_for("client_tree", name=cname, backup=nbackup, server=server) }}?root='+p, function(data) {
				if (!data.results) {
					if (data.notif) {
						$.each(data.notif, function(i, n) {
							notif(n[0], n[1]);
						});
					}
					return;
				}
				$.each(data.results, function(j, c) {
					l = (c.type === "d");
					f = (c.type === "d");
					s = {title: c.name, key: c.parent+c.name, lazy: l, folder: f, uid: c.uid, gid: c.gid, date: c.date, mode: c.mode, size: c.size, inodes: c.inodes};
					r.push(s);
				});
			});
			data.result = r;
			node._isLoading = false;
			node.renderStatus();
		},
		/*
		// TODO: make it recursively loadable
		loadChildren: function(event, data) {
			data.node.visit(function(subNode){
				if( subNode.isUndefined() && subNode.isExpanded() ) {
					subNode.load();
				}
			});
		},
		*/
		scrollParent: $(window),
		renderColumns: function(event, data) {
			var node = data.node;
			$tdList = $(node.tr).find(">td");

			$tdList.eq(1).text(node.data.mode);
			$tdList.eq(2).text(node.data.uid);
			$tdList.eq(3).text(node.data.gid);
			$tdList.eq(4).text(node.data.size);
			$tdList.eq(5).text(node.data.date);
		},
		select: function(event, data) {
			var s = data.tree.getSelectedNodes();
			if (s.length > 0) {
				$("#restore-form").show();
				v = [];
				$.each(s, function(i, n) {
					v.push({key: n.key, folder: n.folder});
				});
				r = {restore:v};
				$("input[name=list]").val(JSON.stringify(r));
			} else {
				$("#restore-form").hide();
				$("input[name=list]").val('');
			}
		}
	});

	var tree = $("#tree").fancytree("getTree");

	$("input[name=search-tree]").keyup(function(e){
		var n,
		leavesOnly = $("#leavesOnly").is(":checked"),
		match = $(this).val();

		if(e && e.which === $.ui.keyCode.ESCAPE || $.trim(match) === ""){
			$("#btnResetSearch").click();
			return;
		}
		if($("#regex").is(":checked")) {
			// Pass function to perform match
			n = tree.filterNodes(function(node) {
				return new RegExp(match, "i").test(node.title);
			}, leavesOnly);
		} else {
			// Pass a string to perform case insensitive matching
			n = tree.filterNodes(match, leavesOnly);
		}
		$("#btnResetSearch").attr("disabled", false);
		$("span#matches").text("(" + n + " matches)");
	});

	$("#btnResetSearch").click(function(e){
		$("input[name=search-tree]").val("");
		$("span#matches").text("");
		tree.clearFilter();
	}).attr("disabled", true);

	$("input#hideMode").change(function(e){
		tree.options.filter.mode = $(this).is(":checked") ? "hide" : "dimm";
		tree.clearFilter();
		$("input[name=search-tree]").keyup();
	});
	$("input#leavesOnly").change(function(e){
		tree.clearFilter();
		$("input[name=search-tree]").keyup();
	});
	$("input#regex").change(function(e){
		tree.clearFilter();
		$("input[name=search-tree]").keyup();
	});

	$("#form-restore").on('submit', function(e) {
		var $preparingFileModal = $("#restore-modal");
		
		$preparingFileModal.modal('toggle');

		$.fileDownload($(this).prop('action'), {
			successCallback: function (url) {
				$preparingFileModal.modal('hide');
			},
			failCallback: function (responseHtml, url) {
				$preparingFileModal.modal('hide');
				$("#error-modal").modal('toggle');
			},
			httpMethod: "POST",
			data: $(this).serialize()
		});
		e.preventDefault();
	});
	$("#btn-clear").on('click', function() {
		tree.visit(function(node){
			node.setSelected(false);
		});
		return false;
	});

