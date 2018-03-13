/*createDate:2015年6月4日
 *create by:lqju
 *description:将下拉框变成支持搜索的文本框的jQuery插件
 示例：
 		<script type="text/javascript" src="/Legion/Platform/JSLibrary/Public/jquery-1.7.1.min.js"></script>
		<script type="text/javascript" src="/GFProject/common/search_tag/search_tag.js"></script>
		<LINK href="/GFProject/common/search_tag/search_tag.css" type=text/css rel=stylesheet>
			
		<script type="text/javascript" size="50">
			$(document).ready(function(){
				var setting = {
					onChange:function(){
						alert('select id changed!');
					}
				};
				// setting参数设置参考
				//var setting = {
				//	divWidth:0,//div宽度，默认于文本框相同
				//	divHeight:0,//div高度，默认180px
				//	url:URL,//异步获取数据的URL
				//	params:params,//异步获取参数
				//	realTime:false,//是否实时获取数据源
				//	onChange:function(){//选项改变时触发的事件
				//		
				//	}
				//}
				
				search_tag.init("targetid",setting);//targetid：下拉框的id
			});
		</script>
		<select id='targetid'>
			<option value='1' selected>测试1</option>
			<option value='2'>测试2</option>
		</select>
*/

var search_tag = {

	currInput: '', //当前被激活的文本框
	currTarget: '', //当前文本框对应的目的标签的ID
	currDiv: '', //下拉选择区域的DIV
	currUl: '', //当前展示数据的UL

	onChange: function() {

	},
	//异步获取数据参数设置
	realTime: false, //是否实时获取数据源
	url: '',//数据源地址：返回的是json数据，数据格式：{text: '',pageTotal: 0,pageSize: 0,pageIndex: 0,data: []}
	params: {},//请求参数

	//分页参数设置
	paging: {
		isPaging: false,//是否分页
		pageSize: 10,//分页大小
		pageIndex: 1,//当前页位置
		pageTotal: 1//分页总数
	},

	inputIdent: '_input_id', //文本框后缀
	divIdent: '_outDiv_id', //DIV后缀
	ulIdent: '_ul_id', //UL后缀

	//控件的各个元素的id和class
	innerDivIdent: 'search_tag_innerDiv',//数据展示区域
	underDivIdent: 'underDivIdent',//控件下方的操作区域
	spanClass: 'search_tag_span',
	outDivClass: 'search_tag_outDiv',
	liClass: 'search_tag_li',
	inputClass: 'form-text', //控制文本框样式

	original_datas: {}, //下拉框的原始数据
	result_datas: {}, //最新搜索结果缓存数据

	_divWidth: 280, //默认DIV宽度
	_divHeight: 400, //默认DIV高度

	//文本检索
	searchTheText: function(text) {
		var pageIndex = this.paging.pageIndex;
		var pageSize = this.paging.pageSize;

		var dataResult = {};//搜索的结果集对象
		if (this.realTime) {//是否是实时获取数据源
			this.params.text = text;//设置查询文本值
			this.params.pageIndex = this.paging.pageIndex;//设置分页位置
			dataResult = this.realTimeSearch();//实时搜索
			this.original_datas[this.currTarget] = dataResult.data;//将数据存储起来
		} else {

			dataResult.data = this.original_datas[this.currTarget].slice(0);//从original_datas里获取缓存数据
			dataResult.text = text;
			dataResult.data = $.grep(dataResult.data, function(obj) {//搜索匹配的数据
				return obj.data_search.indexOf(dataResult.text) > -1 || obj.data_id == '';
			});
			dataResult.pageTotal = Math.max(Math.ceil(dataResult.data.length / pageSize), 1);//计算总页数
			dataResult.pageIndex = pageIndex;//设置分页位置
			dataResult.pageSize = pageSize;//设置分页大小
			dataResult.data = dataResult.data.slice(pageSize * (pageIndex - 1), pageSize * (pageIndex));//截取当前页的结果
		}
		search_tag.paging.pageTotal = dataResult.pageTotal;
		return dataResult;
	},

	//实时搜索
	realTimeSearch: function() {
		var dataResult = {
			text: '',
			pageTotal: 0,
			pageSize: 0,
			pageIndex: 0,
			data: []
		};
		if (this.url != '') {
			$.ajax({
				type: 'post',
				url: this.url,
				async: false,
				dataType: 'json',
				data: this.params,
				contentType: "application/x-www-form-urlencoded; charset=utf-8",
				success: function(result) {
					if (result.errMsg === "") {
						dataResult = result.dataResult;
					} else {
						alert(result.errMsg);
					}
				}
			});
		}
		return dataResult;
	},

	//从下拉列表获取数据源
	getDataFromSelect: function(targetid) {
		var tempData = [];
		$('#' + targetid + '> option').each(function() {
			var temp = {};
			temp.data_id = this.value;
			temp.data_value = $(this).text();
			temp.data_search = $(this).text();
			temp.data_show = $(this).text();
			tempData.push(temp);
		});
		this.original_datas[targetid] = tempData;
		return tempData.length > 0; //返回：是否获取到下拉框的数据
	},

	//异步获取数据源
	getDataSourceAsyn: function(targetid, url, params) {
		if (url != '') {
			$.ajax({
				type: 'post',
				url: url,
				dataType: 'json',
				data: params,
				contentType: "application/x-www-form-urlencoded; charset=utf-8",
				success: function(result) {
					if (result.errMsg === "") {
						search_tag.original_datas[targetid] = result.dataResult;
					} else {
						alert(result.errMsg);
					}
				}
			});
			return true;
		} else {
			return false;
		}
	},

	//生成文本框
	createInput: function(targetid) {

		var inputid = targetid + this.inputIdent,
			inputEle = document.createElement("input"),
			spanEle = document.createElement('span'),
			target_tag = $('#' + targetid)[0];

		inputEle.type = 'text';
		inputEle.name = inputid;
		inputEle.id = inputid;

		//初始化文本框的值为目的标签的值
		if (this.original_datas[targetid]) {
			$.each(this.original_datas[targetid], function() {
				if (this.data_id == target_tag.value) {
					inputEle.value = this.data_value;
					return false;
				}
			});
		}

		//隐藏目的标签
		target_tag.style.display = 'none';

		spanEle.className = this.spanClass;
		spanEle.appendChild(inputEle);

		$('#' + targetid).after(spanEle);
		return inputid;
	},

	//生成数据展示DIV
	createDIV: function(_inputid) {
		var inputEle = $('#' + _inputid),

			divWidth = Math.max(inputEle.width() + 2, this._divWidth), //DIV宽度：不小于文本框
			outDiv = document.createElement("div"),
			innerDiv = document.createElement("div"),
			underDiv = document.createElement("div");
		ul = document.createElement("ul");

		outDiv.id = _inputid + this.divIdent;
		outDiv.className = this.outDivClass;

		innerDiv.id = this.innerDivIdent;
		innerDiv.className = this.innerDivIdent;

		innerDiv.style.width = divWidth + "px";
		innerDiv.style.height = this._divHeight + "px";

		underDiv.id = this.underDivIdent;
		underDiv.className = this.underDivIdent;
		underDiv.onselectstart = function() {
			return false;
		};
		underDiv.innerHTML = "<span id='under_span1' >&nbsp;第&nbsp;<span id='" + _inputid + "under_pageIndex'></span>/<span id='" + _inputid + "under_pageTotal'></span>&nbsp;页&nbsp;</span><span id='under_span2'> <u class='under_firstPage under_u' >首页</u>&nbsp;&nbsp;<u class='under_lastPage under_u' >上一页</u>&nbsp;&nbsp;<u class='under_nextPage under_u' >下一页</u>&nbsp;&nbsp;<u class='under_finalPage under_u' >末页</u>&nbsp;&nbsp;</span>";

		ul.id = _inputid + this.ulIdent;

		innerDiv.appendChild(ul);
		innerDiv.appendChild(underDiv);
		outDiv.appendChild(innerDiv);

		document.body.appendChild(outDiv);
	},

	//生成项目元素
	createLiEle: function(value, name, show) {
		var li = document.createElement("li");
		li.className = this.liClass;
		li.id = value; //目的标签的值
		li.name = name; //关联文本框的值
		li.title = show; //用于项目展示的值
		li.innerHTML = show; //用于项目展示的值
		return li;
	},

	//生成列表项目
	createAllLi: function(data) {
		var tempUl = $('#' + this.currUl);
		tempUl.html("");
		$.each(data, function() {
			var li = search_tag.createLiEle(this.data_id, this.data_value, this.data_show);
			tempUl.append(li);
		});
	},

	//刷新项目列表
	refreshUL: function(targetid) {
		this.currTarget = targetid;
		this.currInput = targetid + this.inputIdent;
		this.currDiv = this.currInput + this.divIdent;
		this.currUl = this.currInput + this.ulIdent;
		var text = $('#' + this.currInput).val();
		var currResult = this.searchTheText(text);
		$('#' + this.currInput + 'under_pageIndex').html(currResult.pageIndex);
		$('#' + this.currInput + 'under_pageTotal').html(currResult.pageTotal);
		this.createAllLi(currResult.data);
	},

	//项目点击触发函数
	choused: function(value, name) {

		$('#' + this.currInput).val(name);
		$('#' + this.currTarget).get(0).value = value;
		//触发onChange事件
		this.onChange();
	},

	//目的标签初始化
	init: function(targetid, setting) {

		var original_tag = $('#' + targetid)[0],
			initDataSuccess = false;

		if (original_tag.style.display != 'none') {
			if (original_tag.type === 'text') {
				initDataSuccess = this.getDataSourceAsyn(targetid, setting.url, setting.params);
			} else if (original_tag.type === 'select-one') {
				initDataSuccess = this.getDataFromSelect(targetid);
			}
		}

		if (initDataSuccess) {

			this._divWidth = (Number(setting.divWidth) > 0 && setting.divWidth) || this._divWidth;

			this._divHeight = (Number(setting.divHeight) > 0 && setting.divHeight) || this._divHeight;


			var _inputid = this.createInput(targetid);
			this.createDIV(_inputid);

			$('#' + _inputid).bind('click input propertychange', function() {
				search_tag.gotoNewIndex(targetid, 1, setting);
				return false;
			});


			$('#' + _inputid).bind('click', function() {

				$('.' + search_tag.outDivClass).hide(); //隐藏所有的项目列表
				$('#' + search_tag.currDiv).show(); //展示当前项目列表

				var inputEle = $('#' + _inputid),
					innerDiv = $('#' + search_tag.currDiv + ">." + search_tag.innerDivIdent),

					offset = inputEle.offset(),
					menuTop = offset.top + inputEle.height() + 2 + 'px', //文本框border:1px
					menuLeft = offset.left + 'px';

				innerDiv.css({
					top: menuTop,
					left: menuLeft
				});
				search_tag.gotoNewIndex(targetid, 1, setting);

				return false;
			});
		}
	},

	initSetting: function(setting) {
		//初始化参数
		search_tag.onChange = (typeof setting.onChange == 'function' && setting.onChange) || function() {};
		search_tag.realTime = setting.realTime || false;
		search_tag.url = setting.url || "";
		search_tag.params = setting.params || {};
		search_tag.paging = setting.paging || {
			isPaging: false,
			pageSize: 15,
			pageIndex: 1,
			pageTotal: 1
		};
	},

	inDiv: function(divid, obj) {
		while (obj.parentNode) {
			if (obj.id == divid) {
				return true;
			}
			obj = obj.parentNode;
		}
		return false;
	},

	//同步文本框及控件的值
	//targetid: 被同步的下拉框的id，空的话就去当前被激活的文本框
	//type：同步类型，如果type==-1，则表示从下拉框同步到文本框
	syncValue: function(targetid, type) {
		
		var currTarget = targetid || this.currTarget;
		var currInput = currTarget + this.inputIdent;

		//如果文本框被清空，则同步清空原标签的直
		//判断是否是反向同步，如果是反向同步，则不清空下拉列表的值
		if (type != -1 && $('#' + currInput).val() == '') {
			//如果是下拉列表，且没有空的选项，则会默认第一个下拉选项
			$('#' + currTarget).get(0).value = "";
			this.onChange();
		}else{
			//反向同步原标签的值到文本框
			var final_result = $('#' + currTarget).val();

			$('#' + currInput).val(final_result); //直接同步

			if (this.original_datas[currTarget]) { //根据id获取value同步
				$.each(this.original_datas[currTarget], function() {
					if (this.data_id == final_result) {
						$('#' + currInput).val(this.data_value);
						return false;
					}
				});
			}
		}
	},

	gotoNewIndex: function(targetid, pageIndex, setting) {
		if (setting) {
			search_tag.initSetting(setting);
		}
		search_tag.paging.pageIndex = pageIndex;
		search_tag.refreshUL(targetid);
	},

	//控件初始化
	control_init: function() {

		$(document).on('click', 'body', function() {
			var e = window.event.srcElement || window.event.target;
			if (e.id != search_tag.innerDivIdent && !search_tag.inDiv(search_tag.underDivIdent, e)) { //如果对象是当前div，则不隐藏
				$('#' + search_tag.currDiv).hide();
				//如果当前事件对象不是项目列表对象，则更新文本框中的值
				if (e.className != search_tag.liClass && search_tag.currTarget != "") {
					search_tag.syncValue();
				}
			}
		});

		//绑定点击下一页的事件
		$(document).on('click', '.under_nextPage', function() {
			if (search_tag.paging.pageTotal > search_tag.paging.pageIndex) {
				search_tag.gotoNewIndex(search_tag.currTarget, ++search_tag.paging.pageIndex);
			}
		});

		//绑定点击上一页的事件
		$(document).on('click', '.under_lastPage', function() {
			if (search_tag.paging.pageIndex > 1) {
				search_tag.gotoNewIndex(search_tag.currTarget, --search_tag.paging.pageIndex);
			}
		});

		//绑定点击首页的事件
		$(document).on('click', '.under_firstPage', function() {
			if (search_tag.paging.pageIndex != 1) {
				search_tag.gotoNewIndex(search_tag.currTarget, 1);
			}
		});

		//绑定点击末页的事件
		$(document).on('click', '.under_finalPage', function() {
			if (search_tag.paging.pageTotal > search_tag.paging.pageIndex) {
				search_tag.gotoNewIndex(search_tag.currTarget, search_tag.paging.pageTotal);
			}
		});

		//绑定列表项目点击事件
		$(document).on('click', '.' + this.liClass, function() {
			search_tag.choused(this.id, this.name);
		});


		//绑定列表项目鼠标进入事件
		$(document).on('mouseenter', '.' + this.liClass, function() {
			$(this).css({
				background: "#2828FF",
				color: "#FFF"
			});
			return false;
		});

		//绑定列表项目鼠标移出事件
		$(document).on('mouseleave', '.' + this.liClass, function() {
			$(this).css({
				background: "",
				color: ""
			});
			return false;
		});
	}
}

//监听按键，解决ie9退格键和del键不触发onpropertychange的问题
document.onkeyup = function(e) {
		var e = e || event,
			currKey = e.keyCode || e.which || e.charCode,
			element = window.event.srcElement || window.event.target;

		//如果当前按键是退格键或者是del键 且 当前元素为 搜索框，则刷新下拉选择域
		//update by lqju 如果当前元素id为空，则也不促发刷新的操作 2016年1月27日
		if ((currKey == 46 || currKey == 8) && element.id != "" && element.id == search_tag.currInput) {
			search_tag.gotoNewIndex(search_tag.currTarget, 1);
		}
	}
	//初始化 搜索控件
search_tag.control_init();